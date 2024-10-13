# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""All the logic for OCI fetching and authentication"""

import base64
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from enum import Enum, auto
from http.client import HTTPResponse
from typing import Callable, Dict, Iterable, List, NamedTuple, Optional, Tuple
from urllib.request import Request

import llnl.util.lang

import spack.config
import spack.mirror
import spack.parser
import spack.util.web

from .image import ImageReference


def _urlopen():
    opener = create_opener()

    def dispatch_open(fullurl, data=None, timeout=None):
        timeout = timeout or spack.config.get("config:connect_timeout", 10)
        return opener.open(fullurl, data, timeout)

    return dispatch_open


OpenType = Callable[..., HTTPResponse]
MaybeOpen = Optional[OpenType]

#: Opener that automatically uses OCI authentication based on mirror config
urlopen: OpenType = llnl.util.lang.Singleton(_urlopen)


SP = r" "
OWS = r"[ \t]*"
BWS = OWS
HTAB = r"\t"
VCHAR = r"\x21-\x7E"
tchar = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]"
token = rf"{tchar}+"
obs_text = r"\x80-\xFF"
qdtext = rf"[{HTAB}{SP}\x21\x23-\x5B\x5D-\x7E{obs_text}]"
quoted_pair = rf"\\([{HTAB}{SP}{VCHAR}{obs_text}])"
quoted_string = rf'"(?:({qdtext}*)|{quoted_pair})*"'


class TokenType(spack.parser.TokenBase):
    AUTH_PARAM = rf"({token}){BWS}={BWS}({token}|{quoted_string})"
    # TOKEN68 = r"([A-Za-z0-9\-._~+/]+=*)"  # todo... support this?
    TOKEN = rf"{tchar}+"
    EQUALS = rf"{BWS}={BWS}"
    COMMA = rf"{OWS},{OWS}"
    SPACE = r" +"
    EOF = r"$"
    ANY = r"."


TOKEN_REGEXES = [rf"(?P<{token}>{token.regex})" for token in TokenType]

ALL_TOKENS = re.compile("|".join(TOKEN_REGEXES))


class State(Enum):
    CHALLENGE = auto()
    AUTH_PARAM_LIST_START = auto()
    AUTH_PARAM = auto()
    NEXT_IN_LIST = auto()
    AUTH_PARAM_OR_SCHEME = auto()


def tokenize(input: str):
    scanner = ALL_TOKENS.scanner(input)  # type: ignore[attr-defined]

    for match in iter(scanner.match, None):  # type: ignore[var-annotated]
        yield spack.parser.Token(
            TokenType.__members__[match.lastgroup],  # type: ignore[attr-defined]
            match.group(),  # type: ignore[attr-defined]
            match.start(),  # type: ignore[attr-defined]
            match.end(),  # type: ignore[attr-defined]
        )


class Challenge:
    __slots__ = ["scheme", "params"]

    def __init__(
        self, scheme: Optional[str] = None, params: Optional[List[Tuple[str, str]]] = None
    ) -> None:
        self.scheme = scheme or ""
        self.params = params or []

    def __repr__(self) -> str:
        return f"Challenge({self.scheme}, {self.params})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Challenge)
            and self.scheme == other.scheme
            and self.params == other.params
        )


def parse_www_authenticate(input: str):
    """Very basic parsing of www-authenticate parsing (RFC7235 section 4.1)
    Notice: this omits token68 support."""

    # auth-scheme      = token
    # auth-param       = token BWS "=" BWS ( token / quoted-string )
    # challenge        = auth-scheme [ 1*SP ( token68 / #auth-param ) ]
    # WWW-Authenticate = 1#challenge

    challenges: List[Challenge] = []

    _unquote = re.compile(quoted_pair).sub
    unquote = lambda s: _unquote(r"\1", s[1:-1])

    mode: State = State.CHALLENGE
    tokens = tokenize(input)

    current_challenge = Challenge()

    def extract_auth_param(input: str) -> Tuple[str, str]:
        key, value = input.split("=", 1)
        key = key.rstrip()
        value = value.lstrip()
        if value.startswith('"'):
            value = unquote(value)
        return key, value

    while True:
        token: spack.parser.Token = next(tokens)

        if mode == State.CHALLENGE:
            if token.kind == TokenType.EOF:
                raise ValueError(token)
            elif token.kind == TokenType.TOKEN:
                current_challenge.scheme = token.value
                mode = State.AUTH_PARAM_LIST_START
            else:
                raise ValueError(token)

        elif mode == State.AUTH_PARAM_LIST_START:
            if token.kind == TokenType.EOF:
                challenges.append(current_challenge)
                break
            elif token.kind == TokenType.COMMA:
                # Challenge without param list, followed by another challenge.
                challenges.append(current_challenge)
                current_challenge = Challenge()
                mode = State.CHALLENGE
            elif token.kind == TokenType.SPACE:
                # A space means it must be followed by param list
                mode = State.AUTH_PARAM
            else:
                raise ValueError(token)

        elif mode == State.AUTH_PARAM:
            if token.kind == TokenType.EOF:
                raise ValueError(token)
            elif token.kind == TokenType.AUTH_PARAM:
                key, value = extract_auth_param(token.value)
                current_challenge.params.append((key, value))
                mode = State.NEXT_IN_LIST
            else:
                raise ValueError(token)

        elif mode == State.NEXT_IN_LIST:
            if token.kind == TokenType.EOF:
                challenges.append(current_challenge)
                break
            elif token.kind == TokenType.COMMA:
                mode = State.AUTH_PARAM_OR_SCHEME
            else:
                raise ValueError(token)

        elif mode == State.AUTH_PARAM_OR_SCHEME:
            if token.kind == TokenType.EOF:
                raise ValueError(token)
            elif token.kind == TokenType.TOKEN:
                challenges.append(current_challenge)
                current_challenge = Challenge(token.value)
                mode = State.AUTH_PARAM_LIST_START
            elif token.kind == TokenType.AUTH_PARAM:
                key, value = extract_auth_param(token.value)
                current_challenge.params.append((key, value))
                mode = State.NEXT_IN_LIST

    return challenges


class RealmServiceScope(NamedTuple):
    realm: str
    service: str
    scope: str


class UsernamePassword(NamedTuple):
    username: str
    password: str


def get_bearer_challenge(challenges: List[Challenge]) -> Optional[RealmServiceScope]:
    # Find a challenge that we can handle (currently only Bearer)
    challenge = next((c for c in challenges if c.scheme == "Bearer"), None)

    if challenge is None:
        return None

    # Get realm / service / scope from challenge
    realm = next((v for k, v in challenge.params if k == "realm"), None)
    service = next((v for k, v in challenge.params if k == "service"), None)
    scope = next((v for k, v in challenge.params if k == "scope"), None)

    if realm is None or service is None or scope is None:
        return None

    return RealmServiceScope(realm, service, scope)


class OCIAuthHandler(urllib.request.BaseHandler):
    def __init__(self, credentials_provider: Callable[[str], Optional[UsernamePassword]]):
        """
        Args:
            credentials_provider: A function that takes a domain and may return a UsernamePassword.
        """
        self.credentials_provider = credentials_provider

        # Cached bearer tokens for a given domain.
        self.cached_tokens: Dict[str, str] = {}

    def obtain_bearer_token(self, registry: str, challenge: RealmServiceScope, timeout) -> str:
        # See https://docs.docker.com/registry/spec/auth/token/

        query = urllib.parse.urlencode(
            {"service": challenge.service, "scope": challenge.scope, "client_id": "spack"}
        )

        parsed = urllib.parse.urlparse(challenge.realm)._replace(
            query=query, fragment="", params=""
        )

        # Don't send credentials over insecure transport.
        if parsed.scheme != "https":
            raise ValueError(
                f"Cannot login to {registry} over insecure {parsed.scheme} connection"
            )

        request = Request(urllib.parse.urlunparse(parsed))

        # I guess we shouldn't cache this, since we don't know
        # the context in which it's used (may depend on config)
        pair = self.credentials_provider(registry)

        if pair is not None:
            encoded = base64.b64encode(f"{pair.username}:{pair.password}".encode("utf-8")).decode(
                "utf-8"
            )
            request.add_unredirected_header("Authorization", f"Basic {encoded}")

        # Do a GET request.
        response = self.parent.open(request, timeout=timeout)

        # Read the response and parse the JSON
        response_json = json.load(response)

        # Get the token from the response
        token = response_json["token"]

        # Remember the last obtained token for this registry
        # Note: we should probably take into account realm, service and scope
        # so we can store multiple tokens for the same registry.
        self.cached_tokens[registry] = token

        return token

    def https_request(self, req: Request):
        # Eagerly add the bearer token to the request if no
        # auth header is set yet, to avoid 401s in multiple
        # requests to the same registry.

        # Use has_header, not .headers, since there are two
        # types of headers (redirected and unredirected)
        if req.has_header("Authorization"):
            return req

        parsed = urllib.parse.urlparse(req.full_url)
        token = self.cached_tokens.get(parsed.netloc)

        if not token:
            return req

        req.add_unredirected_header("Authorization", f"Bearer {token}")
        return req

    def http_error_401(self, req: Request, fp, code, msg, headers):
        # Login failed, avoid infinite recursion where we go back and
        # forth between auth server and registry
        if hasattr(req, "login_attempted"):
            raise spack.util.web.DetailedHTTPError(
                req, code, f"Failed to login: {msg}", headers, fp
            )

        # On 401 Unauthorized, parse the WWW-Authenticate header
        # to determine what authentication is required
        if "WWW-Authenticate" not in headers:
            raise spack.util.web.DetailedHTTPError(
                req, code, "Cannot login to registry, missing WWW-Authenticate header", headers, fp
            )

        header_value = headers["WWW-Authenticate"]

        try:
            challenge = get_bearer_challenge(parse_www_authenticate(header_value))
        except ValueError as e:
            raise spack.util.web.DetailedHTTPError(
                req,
                code,
                f"Cannot login to registry, malformed WWW-Authenticate header: {header_value}",
                headers,
                fp,
            ) from e

        # If there is no bearer challenge, we can't handle it
        if not challenge:
            raise spack.util.web.DetailedHTTPError(
                req,
                code,
                f"Cannot login to registry, unsupported authentication scheme: {header_value}",
                headers,
                fp,
            )

        # Get the token from the auth handler
        try:
            token = self.obtain_bearer_token(
                registry=urllib.parse.urlparse(req.get_full_url()).netloc,
                challenge=challenge,
                timeout=req.timeout,
            )
        except ValueError as e:
            raise spack.util.web.DetailedHTTPError(
                req,
                code,
                f"Cannot login to registry, failed to obtain bearer token: {e}",
                headers,
                fp,
            ) from e

        # Add the token to the request
        req.add_unredirected_header("Authorization", f"Bearer {token}")
        setattr(req, "login_attempted", True)

        return self.parent.open(req, timeout=req.timeout)


def credentials_from_mirrors(
    domain: str, *, mirrors: Optional[Iterable[spack.mirror.Mirror]] = None
) -> Optional[UsernamePassword]:
    """Filter out OCI registry credentials from a list of mirrors."""

    mirrors = mirrors or spack.mirror.MirrorCollection().values()

    for mirror in mirrors:
        # Prefer push credentials over fetch. Unlikely that those are different
        # but our config format allows it.
        for direction in ("push", "fetch"):
            pair = mirror.get_access_pair(direction)
            if pair is None:
                continue
            url = mirror.get_url(direction)
            if not url.startswith("oci://"):
                continue
            try:
                parsed = ImageReference.from_string(url[6:])
            except ValueError:
                continue
            if parsed.domain == domain:
                return UsernamePassword(*pair)
    return None


def create_opener():
    """Create an opener that can handle OCI authentication."""
    opener = urllib.request.OpenerDirector()
    for handler in [
        urllib.request.UnknownHandler(),
        urllib.request.HTTPSHandler(context=spack.util.web.ssl_create_default_context()),
        spack.util.web.SpackHTTPDefaultErrorHandler(),
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPErrorProcessor(),
        OCIAuthHandler(credentials_from_mirrors),
    ]:
        opener.add_handler(handler)
    return opener


def ensure_status(request: urllib.request.Request, response: HTTPResponse, status: int):
    """Raise an error if the response status is not the expected one."""
    if response.status == status:
        return

    raise spack.util.web.DetailedHTTPError(
        request, response.status, response.reason, response.info(), None
    )


def default_retry(f, retries: int = 5, sleep=None):
    sleep = sleep or time.sleep

    def wrapper(*args, **kwargs):
        for i in range(retries):
            try:
                return f(*args, **kwargs)
            except (urllib.error.URLError, TimeoutError) as e:
                # Retry on internal server errors, and rate limit errors
                # Potentially this could take into account the Retry-After header
                # if registries support it
                if i + 1 != retries and (
                    (
                        isinstance(e, urllib.error.HTTPError)
                        and (500 <= e.code < 600 or e.code == 429)
                    )
                    or (
                        isinstance(e, urllib.error.URLError) and isinstance(e.reason, TimeoutError)
                    )
                    or isinstance(e, TimeoutError)
                ):
                    # Exponential backoff
                    sleep(2**i)
                    continue
                raise

    return wrapper
