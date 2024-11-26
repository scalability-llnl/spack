# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import base64
import email.message
import hashlib
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Callable, Dict, List, Optional, Pattern, Tuple
from urllib.request import Request

import spack.oci.oci
from spack.oci.image import Digest
from spack.oci.opener import OCIAuthHandler


class MockHTTPResponse(io.IOBase):
    """This is a mock HTTP response, which implements part of http.client.HTTPResponse"""

    def __init__(self, status, reason, headers=None, body=None):
        self.msg = None
        self.version = 11
        self.url = None
        self.headers = email.message.EmailMessage()
        self.status = status
        self.code = status
        self.reason = reason
        self.debuglevel = 0
        self._body = body

        if headers is not None:
            for key, value in headers.items():
                self.headers[key] = value

    @classmethod
    def with_json(cls, status, reason, headers=None, body=None):
        """Create a mock HTTP response with JSON string as body"""
        body = io.BytesIO(json.dumps(body).encode("utf-8"))
        return cls(status, reason, headers, body)

    def read(self, *args, **kwargs):
        return self._body.read(*args, **kwargs)

    def getheader(self, name, default=None):
        self.headers.get(name, default)

    def getheaders(self):
        return self.headers.items()

    def fileno(self):
        return 0

    def getcode(self):
        return self.status

    def info(self):
        return self.headers


class MiddlewareError(Exception):
    """Thrown in a handler to return a response early."""

    def __init__(self, response: MockHTTPResponse):
        self.response = response


class Router:
    """This class is a small router for requests to the OCI registry.

    It is used to dispatch requests to a handler, and middleware can be
    used to transform requests, as well as return responses early
    (e.g. for authentication)."""

    def __init__(self) -> None:
        self.routes: List[Tuple[str, Pattern, Callable]] = []
        self.middleware: List[Callable[[Request], Request]] = []

    def handle(self, req: Request) -> MockHTTPResponse:
        """Dispatch a request to a handler."""
        result = urllib.parse.urlparse(req.full_url)

        # Apply middleware
        try:
            for handler in self.middleware:
                req = handler(req)
        except MiddlewareError as e:
            return e.response

        for method, path_regex, handler in self.routes:
            if method != req.get_method():
                continue
            match = re.fullmatch(path_regex, result.path)
            if not match:
                continue

            return handler(req, **match.groupdict())

        return MockHTTPResponse(404, "Not found")

    def register(self, method, path: str, handler: Callable):
        self.routes.append((method, re.compile(path), handler))

    def add_middleware(self, handler: Callable[[Request], Request]):
        self.middleware.append(handler)


class DummyServer:
    def __init__(self, domain: str) -> None:
        # The domain of the server, e.g. "registry.example.com"
        self.domain = domain

        # List of (method, url) tuples
        self.requests: List[Tuple[str, str]] = []

        # Dispatches requests to handlers
        self.router = Router()

        # Always install a request logger
        self.router.add_middleware(self.log_request)

    def handle(self, req: Request) -> MockHTTPResponse:
        return self.router.handle(req)

    def log_request(self, req: Request):
        path = urllib.parse.urlparse(req.full_url).path
        self.requests.append((req.get_method(), path))
        return req

    def clear_log(self):
        self.requests = []


class InMemoryOCIRegistry(DummyServer):
    """This implements the basic OCI registry API, but in memory.

    It supports two types of blob uploads:
    1. POST + PUT: the client first starts a session with POST, then does a large PUT request
    2. POST: the client does a single POST request with the whole blob

    Option 2 is not supported by all registries, so we allow to disable it,
    with allow_single_post=False.

    A third option is to use the chunked upload, but this is not implemented here, because
    it's typically a major performance hit in upload speed, so we're not using it in Spack."""

    def __init__(
        self, domain: str, allow_single_post: bool = True, tags_per_page: int = 100
    ) -> None:
        super().__init__(domain)
        self.router.register("GET", r"/v2/", self.index)
        self.router.register("HEAD", r"/v2/(?P<name>.+)/blobs/(?P<digest>.+)", self.head_blob)
        self.router.register("POST", r"/v2/(?P<name>.+)/blobs/uploads/", self.start_session)
        self.router.register("PUT", r"/upload", self.put_session)
        self.router.register("PUT", r"/v2/(?P<name>.+)/manifests/(?P<ref>.+)", self.put_manifest)
        self.router.register("GET", r"/v2/(?P<name>.+)/manifests/(?P<ref>.+)", self.get_manifest)
        self.router.register("GET", r"/v2/(?P<name>.+)/blobs/(?P<digest>.+)", self.get_blob)
        self.router.register("GET", r"/v2/(?P<name>.+)/tags/list", self.list_tags)

        # If True, allow single POST upload, not all registries support this
        self.allow_single_post = allow_single_post

        # How many tags are returned in a single request
        self.tags_per_page = tags_per_page

        # Used for POST + PUT upload. This is a map from session ID to image name
        self.sessions: Dict[str, str] = {}

        # Set of sha256:... digests that are known to the registry
        self.blobs: Dict[str, bytes] = {}

        # Map from (name, tag) to manifest
        self.manifests: Dict[Tuple[str, str], dict] = {}

    def index(self, req: Request):
        return MockHTTPResponse.with_json(200, "OK", body={})

    def head_blob(self, req: Request, name: str, digest: str):
        if digest in self.blobs:
            return MockHTTPResponse(200, "OK", headers={"Content-Length": "1234"})
        return MockHTTPResponse(404, "Not found")

    def get_blob(self, req: Request, name: str, digest: str):
        if digest in self.blobs:
            return MockHTTPResponse(200, "OK", body=io.BytesIO(self.blobs[digest]))
        return MockHTTPResponse(404, "Not found")

    def start_session(self, req: Request, name: str):
        id = str(uuid.uuid4())
        self.sessions[id] = name

        # Check if digest is present (single monolithic upload)
        result = urllib.parse.urlparse(req.full_url)
        query = urllib.parse.parse_qs(result.query)

        if self.allow_single_post and "digest" in query:
            return self.handle_upload(
                req, name=name, digest=Digest.from_string(query["digest"][0])
            )

        return MockHTTPResponse(202, "Accepted", headers={"Location": f"/upload?uuid={id}"})

    def put_session(self, req: Request):
        # Do the upload.
        result = urllib.parse.urlparse(req.full_url)
        query = urllib.parse.parse_qs(result.query)

        # uuid param should be preserved, and digest should be present
        assert "uuid" in query and len(query["uuid"]) == 1
        assert "digest" in query and len(query["digest"]) == 1

        id = query["uuid"][0]
        assert id in self.sessions

        name, digest = self.sessions[id], Digest.from_string(query["digest"][0])

        response = self.handle_upload(req, name=name, digest=digest)

        # End the session
        del self.sessions[id]

        return response

    def put_manifest(self, req: Request, name: str, ref: str):
        # In requests, Python runs header.capitalize().
        content_type = req.get_header("Content-type")
        assert content_type in spack.oci.oci.all_content_type

        index_or_manifest = json.loads(self._require_data(req))

        # Verify that we have all blobs (layers for manifest, manifests for index)
        if content_type in spack.oci.oci.manifest_content_type:
            for layer in index_or_manifest["layers"]:
                assert layer["digest"] in self.blobs, "Missing blob while uploading manifest"

        else:
            for manifest in index_or_manifest["manifests"]:
                assert (
                    name,
                    manifest["digest"],
                ) in self.manifests, "Missing manifest while uploading index"

        self.manifests[(name, ref)] = index_or_manifest

        return MockHTTPResponse(
            201, "Created", headers={"Location": f"/v2/{name}/manifests/{ref}"}
        )

    def get_manifest(self, req: Request, name: str, ref: str):
        if (name, ref) not in self.manifests:
            return MockHTTPResponse(404, "Not found")

        manifest_or_index = self.manifests[(name, ref)]

        return MockHTTPResponse.with_json(
            200,
            "OK",
            headers={"Content-type": manifest_or_index["mediaType"]},
            body=manifest_or_index,
        )

    def _require_data(self, req: Request) -> bytes:
        """Extract request.data, it's type remains a mystery"""
        assert req.data is not None

        if hasattr(req.data, "read"):
            return req.data.read()
        elif isinstance(req.data, bytes):
            return req.data

        raise ValueError("req.data should be bytes or have a read() method")

    def handle_upload(self, req: Request, name: str, digest: Digest):
        """Verify the digest, save the blob, return created status"""
        data = self._require_data(req)
        assert hashlib.sha256(data).hexdigest() == digest.digest
        self.blobs[str(digest)] = data
        return MockHTTPResponse(201, "Created", headers={"Location": f"/v2/{name}/blobs/{digest}"})

    def list_tags(self, req: Request, name: str):
        # Paginate using Link headers, this was added to the spec in the following commit:
        # https://github.com/opencontainers/distribution-spec/commit/2ed79d930ecec11dd755dc8190409a3b10f01ca9

        # List all tags, exclude digests.
        all_tags = sorted(
            _tag for _name, _tag in self.manifests.keys() if _name == name and ":" not in _tag
        )

        query = urllib.parse.parse_qs(urllib.parse.urlparse(req.full_url).query)

        n = int(query["n"][0]) if "n" in query else self.tags_per_page

        if "last" in query:
            try:
                offset = all_tags.index(query["last"][0]) + 1
            except ValueError:
                return MockHTTPResponse(404, "Not found")
        else:
            offset = 0

        tags = all_tags[offset : offset + n]

        if offset + n < len(all_tags):
            headers = {"Link": f'</v2/{name}/tags/list?last={tags[-1]}&n={n}>; rel="next"'}
        else:
            headers = None

        return MockHTTPResponse.with_json(200, "OK", headers=headers, body={"tags": tags})


class DummyServerUrllibHandler(urllib.request.BaseHandler):
    """Glue between urllib and DummyServer, routing requests to
    the correct mock server for a given domain."""

    def __init__(self) -> None:
        self.servers: Dict[str, DummyServer] = {}

    def add_server(self, domain: str, api: DummyServer):
        self.servers[domain] = api
        return self

    def https_open(self, req: Request):
        domain = urllib.parse.urlparse(req.full_url).netloc

        if domain not in self.servers:
            return MockHTTPResponse(404, "Not found")

        return self.servers[domain].handle(req)


class InMemoryOCIRegistryWithAuth(InMemoryOCIRegistry):
    """This is another in-memory OCI registry, but it requires authentication."""

    def __init__(
        self, domain, token: Optional[str], realm: str, allow_single_post: bool = True
    ) -> None:
        super().__init__(domain, allow_single_post)
        self.token = token  # token to accept
        self.realm = realm  # url to the authorization server
        self.router.add_middleware(self.authenticate)

    def authenticate(self, req: Request):
        # Any request needs an Authorization header
        authorization = req.get_header("Authorization")

        if authorization is None:
            raise MiddlewareError(self.unauthorized())

        # Ensure that the token is correct
        assert authorization.startswith("Bearer ")
        token = authorization[7:]

        if token != self.token:
            raise MiddlewareError(self.unauthorized())

        return req

    def unauthorized(self):
        return MockHTTPResponse(
            401,
            "Unauthorized",
            {
                "www-authenticate": f'Bearer realm="{self.realm}",'
                f'service="{self.domain}",'
                'scope="repository:spack-registry:pull,push"'
            },
        )


class MockBearerTokenServer(DummyServer):
    """Simulates a basic server that hands out bearer tokens
    at the /login endpoint for the following services:
    public.example.com, which doesn't require Basic Auth
    private.example.com, which requires Basic Auth, with user:pass
    """

    def __init__(self, domain: str) -> None:
        super().__init__(domain)
        self.router.register("GET", "/login", self.login)

    def login(self, req: Request):
        url = urllib.parse.urlparse(req.full_url)
        query_params = urllib.parse.parse_qs(url.query)

        # Verify query params, from the www-authenticate header
        assert query_params["client_id"] == ["spack"]
        assert len(query_params["service"]) == 1
        assert query_params["scope"] == ["repository:spack-registry:pull,push"]

        service = query_params["service"][0]

        if service == "public.example.com":
            return self.public_auth(req)
        elif service == "private.example.com":
            return self.private_auth(req)

        return MockHTTPResponse(404, "Not found")

    def public_auth(self, req: Request):
        # No need to login with username and password for the public registry
        assert req.get_header("Authorization") is None
        return MockHTTPResponse.with_json(200, "OK", body={"token": "public_token"})

    def private_auth(self, req: Request):
        # For the private registry we need to login with username and password
        auth_value = req.get_header("Authorization")

        if (
            auth_value is None
            or not auth_value.startswith("Basic ")
            or base64.b64decode(auth_value[6:]) != b"user:pass"
        ):
            return MockHTTPResponse(401, "Unauthorized")

        return MockHTTPResponse.with_json(200, "OK", body={"token": "private_token"})


def create_opener(*servers: DummyServer, credentials_provider=None):
    """Creates a mock opener, that can be used to fake requests to a list
    of servers."""
    opener = urllib.request.OpenerDirector()
    handler = DummyServerUrllibHandler()
    for server in servers:
        handler.add_server(server.domain, server)
    opener.add_handler(handler)
    opener.add_handler(urllib.request.HTTPDefaultErrorHandler())
    opener.add_handler(urllib.request.HTTPErrorProcessor())
    if credentials_provider is not None:
        opener.add_handler(OCIAuthHandler(credentials_provider))
    return opener
