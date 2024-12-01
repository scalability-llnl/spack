# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import hashlib
import json
import random
import urllib.error
import urllib.parse
import urllib.request
from urllib.request import Request

import pytest

import spack.mirror
from spack.oci.image import Digest, ImageReference, default_config, default_manifest
from spack.oci.oci import (
    copy_missing_layers,
    get_manifest_and_config,
    image_from_mirror,
    list_tags,
    upload_blob,
    upload_manifest,
)
from spack.oci.opener import (
    Challenge,
    RealmServiceScope,
    UsernamePassword,
    credentials_from_mirrors,
    default_retry,
    get_bearer_challenge,
    parse_www_authenticate,
)
from spack.test.oci.mock_registry import (
    DummyServer,
    DummyServerUrllibHandler,
    InMemoryOCIRegistry,
    InMemoryOCIRegistryWithAuth,
    MiddlewareError,
    MockBearerTokenServer,
    MockHTTPResponse,
    create_opener,
)


def test_parse_www_authenticate():
    """Test parsing of valid WWW-Authenticate header, check whether it's
    decomposed into a list of challenges with correct scheme and parameters
    according to RFC 7235 section 4.1"""
    www_authenticate = 'Bearer realm="https://spack.io/authenticate",service="spack-registry",scope="repository:spack-registry:pull,push"'
    assert parse_www_authenticate(www_authenticate) == [
        Challenge(
            "Bearer",
            [
                ("realm", "https://spack.io/authenticate"),
                ("service", "spack-registry"),
                ("scope", "repository:spack-registry:pull,push"),
            ],
        )
    ]

    assert parse_www_authenticate("Bearer") == [Challenge("Bearer")]
    assert parse_www_authenticate("MethodA, MethodB,MethodC") == [
        Challenge("MethodA"),
        Challenge("MethodB"),
        Challenge("MethodC"),
    ]

    assert parse_www_authenticate(
        'Digest realm="Digest Realm", nonce="1234567890", algorithm=MD5, qop="auth"'
    ) == [
        Challenge(
            "Digest",
            [
                ("realm", "Digest Realm"),
                ("nonce", "1234567890"),
                ("algorithm", "MD5"),
                ("qop", "auth"),
            ],
        )
    ]

    assert parse_www_authenticate(
        r'Newauth realm="apps", type=1, title="Login to \"apps\"", Basic realm="simple"'
    ) == [
        Challenge("Newauth", [("realm", "apps"), ("type", "1"), ("title", 'Login to "apps"')]),
        Challenge("Basic", [("realm", "simple")]),
    ]


@pytest.mark.parametrize(
    "invalid_str",
    [
        # Not comma separated
        "SchemeA SchemeB SchemeC",
        # Unexpected eof
        "SchemeA, SchemeB, SchemeC, ",
        # Invalid auth param or scheme
        r"Scheme x=y, ",
        # Unexpected eof
        "Scheme key=",
        # Invalid token
        r'"Bearer"',
        # Invalid token
        r'Scheme"xyz"',
        # No auth param
        r"Scheme ",
    ],
)
def test_invalid_www_authenticate(invalid_str):
    with pytest.raises(ValueError):
        parse_www_authenticate(invalid_str)


def test_get_bearer_challenge():
    """Test extracting Bearer challenge from a list of challenges"""

    # Only an incomplete bearer challenge, missing service and scope, not usable.
    assert (
        get_bearer_challenge(
            [
                Challenge("Bearer", [("realm", "https://spack.io/authenticate")]),
                Challenge("Basic", [("realm", "simple")]),
                Challenge(
                    "Digest",
                    [
                        ("realm", "Digest Realm"),
                        ("nonce", "1234567890"),
                        ("algorithm", "MD5"),
                        ("qop", "auth"),
                    ],
                ),
            ]
        )
        is None
    )

    # Multiple challenges, should pick the bearer one.
    assert get_bearer_challenge(
        [
            Challenge(
                "Dummy",
                [("realm", "https://example.com/"), ("service", "service"), ("scope", "scope")],
            ),
            Challenge(
                "Bearer",
                [
                    ("realm", "https://spack.io/authenticate"),
                    ("service", "spack-registry"),
                    ("scope", "repository:spack-registry:pull,push"),
                ],
            ),
        ]
    ) == RealmServiceScope(
        "https://spack.io/authenticate", "spack-registry", "repository:spack-registry:pull,push"
    )


@pytest.mark.parametrize(
    "image_ref,token",
    [
        ("public.example.com/spack-registry:latest", "public_token"),
        ("private.example.com/spack-registry:latest", "private_token"),
    ],
)
def test_automatic_oci_authentication(image_ref, token):
    image = ImageReference.from_string(image_ref)

    def credentials_provider(domain: str):
        return UsernamePassword("user", "pass") if domain == "private.example.com" else None

    opener = create_opener(
        InMemoryOCIRegistryWithAuth(
            image.domain, token=token, realm="https://auth.example.com/login"
        ),
        MockBearerTokenServer("auth.example.com"),
        credentials_provider=credentials_provider,
    )

    # Run this twice, as it will triggers a code path that caches the bearer token
    assert opener.open(image.endpoint()).status == 200
    assert opener.open(image.endpoint()).status == 200


def test_wrong_credentials():
    """Test that when wrong credentials are rejected by the auth server, we
    get a 401 error."""
    credentials_provider = lambda domain: UsernamePassword("wrong", "wrong")
    image = ImageReference.from_string("private.example.com/image")
    opener = create_opener(
        InMemoryOCIRegistryWithAuth(
            image.domain, token="something", realm="https://auth.example.com/login"
        ),
        MockBearerTokenServer("auth.example.com"),
        credentials_provider=credentials_provider,
    )

    with pytest.raises(urllib.error.HTTPError) as e:
        opener.open(image.endpoint())

    assert e.value.getcode() == 401


def test_wrong_bearer_token_returned_by_auth_server():
    """When the auth server returns a wrong bearer token, we should get a 401 error
    when the request we attempt fails. We shouldn't go in circles getting a 401 from
    the registry, then a non-working token from the auth server, then a 401 from the
    registry, etc."""
    image = ImageReference.from_string("private.example.com/image")
    opener = create_opener(
        InMemoryOCIRegistryWithAuth(
            image.domain,
            token="other_token_than_token_server_provides",
            realm="https://auth.example.com/login",
        ),
        MockBearerTokenServer("auth.example.com"),
        credentials_provider=lambda domain: UsernamePassword("user", "pass"),
    )

    with pytest.raises(urllib.error.HTTPError) as e:
        opener.open(image.endpoint())

    assert e.value.getcode() == 401


class TrivialAuthServer(DummyServer):
    """A trivial auth server that hands out a bearer token at GET /login."""

    def __init__(self, domain: str, token: str) -> None:
        super().__init__(domain)
        self.router.register("GET", "/login", self.login)
        self.token = token

    def login(self, req: Request):
        return MockHTTPResponse.with_json(200, "OK", body={"token": self.token})


def test_registry_with_short_lived_bearer_tokens():
    """An issued bearer token is mostly opaque to the client, but typically
    it embeds a short-lived expiration date. To speed up requests to a registry,
    it's good not to authenticate on every request, but to cache the bearer token,
    however: we have to deal with the case of an expired bearer token.

    Here we test that when the bearer token expires, we authenticate again, and
    when the token is still valid, we don't re-authenticate."""

    image = ImageReference.from_string("private.example.com/image")
    credentials_provider = lambda domain: UsernamePassword("user", "pass")

    auth_server = TrivialAuthServer("auth.example.com", token="token")
    registry_server = InMemoryOCIRegistryWithAuth(
        image.domain, token="token", realm="https://auth.example.com/login"
    )
    urlopen = create_opener(
        registry_server, auth_server, credentials_provider=credentials_provider
    ).open

    # First request, should work with token "token"
    assert urlopen(image.endpoint()).status == 200

    # Invalidate the token on the registry
    registry_server.token = "new_token"
    auth_server.token = "new_token"

    # Second request: reusing the cached token should fail
    # but in the background we will get a new token from the auth server
    assert urlopen(image.endpoint()).status == 200

    # Subsequent requests should work with the same token, let's do two more
    assert urlopen(image.endpoint()).status == 200
    assert urlopen(image.endpoint()).status == 200

    # And finally, we should see that we've issues exactly two requests to the auth server
    assert auth_server.requests == [("GET", "/login"), ("GET", "/login")]

    # Whereas we've done more requests to the registry
    assert registry_server.requests == [
        ("GET", "/v2/"),  # 1: without bearer token
        ("GET", "/v2/"),  # 2: retry with bearer token
        ("GET", "/v2/"),  # 3: with incorrect bearer token
        ("GET", "/v2/"),  # 4: retry with new bearer token
        ("GET", "/v2/"),  # 5: with recyled correct bearer token
        ("GET", "/v2/"),  # 6: with recyled correct bearer token
    ]


class InMemoryRegistryWithUnsupportedAuth(InMemoryOCIRegistry):
    """A registry that does set a WWW-Authenticate header, but
    with a challenge we don't support."""

    def __init__(self, domain: str, allow_single_post: bool = True, www_authenticate=None) -> None:
        self.www_authenticate = www_authenticate
        super().__init__(domain, allow_single_post)
        self.router.add_middleware(self.unsupported_auth_method)

    def unsupported_auth_method(self, req: Request):
        headers = {}
        if self.www_authenticate:
            headers["WWW-Authenticate"] = self.www_authenticate
        raise MiddlewareError(MockHTTPResponse(401, "Unauthorized", headers=headers))


@pytest.mark.parametrize(
    "www_authenticate,error_message",
    [
        # missing service and scope
        ('Bearer realm="https://auth.example.com/login"', "unsupported authentication scheme"),
        # we don't do basic auth
        ('Basic realm="https://auth.example.com/login"', "unsupported authentication scheme"),
        # multiple unsupported challenges
        (
            "CustomChallenge method=unsupported, OtherChallenge method=x,param=y",
            "unsupported authentication scheme",
        ),
        # no challenge
        (None, "missing WWW-Authenticate header"),
        # malformed challenge, missing quotes
        ("Bearer realm=https://auth.example.com", "malformed WWW-Authenticate header"),
        # http instead of https
        ('Bearer realm="http://auth.example.com",scope=x,service=y', "insecure http connection"),
    ],
)
def test_auth_method_we_cannot_handle_is_error(www_authenticate, error_message):
    # We can only handle WWW-Authenticate with a Bearer challenge
    image = ImageReference.from_string("private.example.com/image")
    urlopen = create_opener(
        InMemoryRegistryWithUnsupportedAuth(image.domain, www_authenticate=www_authenticate),
        TrivialAuthServer("auth.example.com", token="token"),
        credentials_provider=lambda domain: UsernamePassword("user", "pass"),
    ).open

    with pytest.raises(urllib.error.HTTPError, match=error_message) as e:
        urlopen(image.endpoint())
    assert e.value.getcode() == 401


# Parametrize over single POST vs POST + PUT.
@pytest.mark.parametrize("client_single_request", [True, False])
@pytest.mark.parametrize("server_single_request", [True, False])
def test_oci_registry_upload(tmpdir, client_single_request, server_single_request):
    opener = urllib.request.OpenerDirector()
    opener.add_handler(
        DummyServerUrllibHandler().add_server(
            "example.com", InMemoryOCIRegistry(server_single_request)
        )
    )
    opener.add_handler(urllib.request.HTTPDefaultErrorHandler())
    opener.add_handler(urllib.request.HTTPErrorProcessor())

    # Create a small blob
    blob = tmpdir.join("blob")
    blob.write("Hello world!")

    image = ImageReference.from_string("example.com/image:latest")
    digest = Digest.from_sha256(hashlib.sha256(blob.read_binary()).hexdigest())

    # Set small file size larger than the blob iff we're doing single request
    small_file_size = 1024 if client_single_request else 0

    # Upload once, should actually upload
    assert upload_blob(
        ref=image,
        file=blob.strpath,
        digest=digest,
        small_file_size=small_file_size,
        _urlopen=opener.open,
    )

    # Second time should exit as it exists
    assert not upload_blob(
        ref=image,
        file=blob.strpath,
        digest=digest,
        small_file_size=small_file_size,
        _urlopen=opener.open,
    )

    # Force upload should upload again
    assert upload_blob(
        ref=image,
        file=blob.strpath,
        digest=digest,
        force=True,
        small_file_size=small_file_size,
        _urlopen=opener.open,
    )


def test_copy_missing_layers(tmpdir, config):
    """Test copying layers from one registry to another.
    Creates 3 blobs, 1 config and 1 manifest in registry A
    and copies layers to registry B. Then checks that all
    layers are present in registry B. Finally it runs the copy
    again and checks that no new layers are uploaded."""

    # NOTE: config fixture is used to disable default source mirrors
    # which are used in Stage(...). Otherwise this test doesn't really
    # rely on globals.

    src = ImageReference.from_string("a.example.com/image:x")
    dst = ImageReference.from_string("b.example.com/image:y")

    src_registry = InMemoryOCIRegistry(src.domain)
    dst_registry = InMemoryOCIRegistry(dst.domain)

    urlopen = create_opener(src_registry, dst_registry).open

    # TODO: make it a bit easier to create bunch of blobs + config + manifest?

    # Create a few blobs and a config file
    blobs = [tmpdir.join(f"blob{i}") for i in range(3)]

    for i, blob in enumerate(blobs):
        blob.write(f"Blob {i}")

    digests = [
        Digest.from_sha256(hashlib.sha256(blob.read_binary()).hexdigest()) for blob in blobs
    ]

    config = default_config(architecture="amd64", os="linux")
    configfile = tmpdir.join("config.json")
    configfile.write(json.dumps(config))
    config_digest = Digest.from_sha256(hashlib.sha256(configfile.read_binary()).hexdigest())

    for blob, digest in zip(blobs, digests):
        upload_blob(src, blob.strpath, digest, _urlopen=urlopen)
    upload_blob(src, configfile.strpath, config_digest, _urlopen=urlopen)

    # Then create a manifest referencing them
    manifest = default_manifest()

    for blob, digest in zip(blobs, digests):
        manifest["layers"].append(
            {
                "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
                "digest": str(digest),
                "size": blob.size(),
            }
        )

    manifest["config"] = {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": str(config_digest),
        "size": configfile.size(),
    }

    upload_manifest(src, manifest, _urlopen=urlopen)

    # Finally, copy the image from src to dst
    copy_missing_layers(src, dst, architecture="amd64", _urlopen=urlopen)

    # Check that all layers (not config) were copied and identical
    assert len(dst_registry.blobs) == len(blobs)
    for blob, digest in zip(blobs, digests):
        assert dst_registry.blobs.get(str(digest)) == blob.read_binary()

    is_upload = lambda method, path: method == "POST" and path == "/v2/image/blobs/uploads/"
    is_exists = lambda method, path: method == "HEAD" and path.startswith("/v2/image/blobs/")

    # Check that exactly 3 uploads were initiated, and that we don't do
    # double existence checks when uploading.
    assert sum(is_upload(method, path) for method, path in dst_registry.requests) == 3
    assert sum(is_exists(method, path) for method, path in dst_registry.requests) == 3

    # Check that re-uploading skips existing layers.
    dst_registry.clear_log()
    copy_missing_layers(src, dst, architecture="amd64", _urlopen=urlopen)

    # Check that no uploads were initiated, only existence checks were done.
    assert sum(is_upload(method, path) for method, path in dst_registry.requests) == 0
    assert sum(is_exists(method, path) for method, path in dst_registry.requests) == 3


def test_image_from_mirror():
    mirror = spack.mirror.Mirror("oci://example.com/image")
    assert image_from_mirror(mirror) == ImageReference.from_string("example.com/image")


def test_image_reference_str():
    """Test that with_digest() works with Digest and str."""
    digest_str = f"sha256:{1234:064x}"
    digest = Digest.from_string(digest_str)

    img = ImageReference.from_string("example.com/image")

    assert str(img.with_digest(digest)) == f"example.com/image:latest@{digest}"
    assert str(img.with_digest(digest_str)) == f"example.com/image:latest@{digest}"
    assert str(img.with_tag("hello")) == "example.com/image:hello"
    assert str(img.with_tag("hello").with_digest(digest)) == f"example.com/image:hello@{digest}"


@pytest.mark.parametrize(
    "image",
    [
        # white space issue
        " example.com/image",
        # not alpha-numeric
        "hello#world:latest",
    ],
)
def test_image_reference_invalid(image):
    with pytest.raises(ValueError, match="Invalid image reference"):
        ImageReference.from_string(image)


def test_default_credentials_provider():
    """The default credentials provider uses a collection of configured
    mirrors."""

    mirrors = [
        # OCI mirror with push credentials
        spack.mirror.Mirror(
            {"url": "oci://a.example.com/image", "push": {"access_pair": ["user.a", "pass.a"]}}
        ),
        # Not an OCI mirror
        spack.mirror.Mirror(
            {"url": "https://b.example.com/image", "access_pair": ["user.b", "pass.b"]}
        ),
        # No credentials
        spack.mirror.Mirror("oci://c.example.com/image"),
        # Top-level credentials
        spack.mirror.Mirror(
            {"url": "oci://d.example.com/image", "access_pair": ["user.d", "pass.d"]}
        ),
        # Dockerhub short reference
        spack.mirror.Mirror(
            {"url": "oci://user/image", "access_pair": ["dockerhub_user", "dockerhub_pass"]}
        ),
        # Localhost (not a dockerhub short reference)
        spack.mirror.Mirror(
            {"url": "oci://localhost/image", "access_pair": ["user.localhost", "pass.localhost"]}
        ),
    ]

    assert credentials_from_mirrors("a.example.com", mirrors=mirrors) == UsernamePassword(
        "user.a", "pass.a"
    )
    assert credentials_from_mirrors("b.example.com", mirrors=mirrors) is None
    assert credentials_from_mirrors("c.example.com", mirrors=mirrors) is None
    assert credentials_from_mirrors("d.example.com", mirrors=mirrors) == UsernamePassword(
        "user.d", "pass.d"
    )
    assert credentials_from_mirrors("index.docker.io", mirrors=mirrors) == UsernamePassword(
        "dockerhub_user", "dockerhub_pass"
    )
    assert credentials_from_mirrors("localhost", mirrors=mirrors) == UsernamePassword(
        "user.localhost", "pass.localhost"
    )


def test_manifest_index(tmpdir):
    """Test obtaining manifest + config from a registry
    that has an index"""
    urlopen = create_opener(InMemoryOCIRegistry("registry.example.com")).open

    img = ImageReference.from_string("registry.example.com/image")

    # Create two config files and manifests, for different architectures
    manifest_descriptors = []
    manifest_and_config = {}
    for arch in ("amd64", "arm64"):
        file = tmpdir.join(f"config_{arch}.json")
        config = default_config(architecture=arch, os="linux")
        file.write(json.dumps(config))
        config_digest = Digest.from_sha256(hashlib.sha256(file.read_binary()).hexdigest())
        assert upload_blob(img, file, config_digest, _urlopen=urlopen)
        manifest = {
            "schemaVersion": 2,
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "config": {
                "mediaType": "application/vnd.oci.image.config.v1+json",
                "digest": str(config_digest),
                "size": file.size(),
            },
            "layers": [],
        }
        manifest_digest, manifest_size = upload_manifest(
            img, manifest, tag=False, _urlopen=urlopen
        )

        manifest_descriptors.append(
            {
                "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "platform": {"architecture": arch, "os": "linux"},
                "digest": str(manifest_digest),
                "size": manifest_size,
            }
        )

        manifest_and_config[arch] = (manifest, config)

    # And a single index.
    index = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.index.v1+json",
        "manifests": manifest_descriptors,
    }

    upload_manifest(img, index, tag=True, _urlopen=urlopen)

    # Check that we fetcht the correct manifest and config for each architecture
    for arch in ("amd64", "arm64"):
        assert (
            get_manifest_and_config(img, architecture=arch, _urlopen=urlopen)
            == manifest_and_config[arch]
        )

    # Also test max recursion
    with pytest.raises(Exception, match="Maximum recursion depth reached"):
        get_manifest_and_config(img, architecture="amd64", recurse=0, _urlopen=urlopen)


class BrokenServer(DummyServer):
    """Dummy server that returns 500 and 429 errors twice before succeeding"""

    def __init__(self, domain: str) -> None:
        super().__init__(domain)
        self.router.register("GET", r"/internal-server-error/", self.internal_server_error_twice)
        self.router.register("GET", r"/rate-limit/", self.rate_limit_twice)
        self.router.register("GET", r"/not-found/", self.not_found)
        self.count_500 = 0
        self.count_429 = 0

    def internal_server_error_twice(self, request: Request):
        self.count_500 += 1
        if self.count_500 < 3:
            return MockHTTPResponse(500, "Internal Server Error")
        else:
            return MockHTTPResponse(200, "OK")

    def rate_limit_twice(self, request: Request):
        self.count_429 += 1
        if self.count_429 < 3:
            return MockHTTPResponse(429, "Rate Limit Exceeded")
        else:
            return MockHTTPResponse(200, "OK")

    def not_found(self, request: Request):
        return MockHTTPResponse(404, "Not Found")


@pytest.mark.parametrize(
    "url,max_retries,expect_failure,expect_requests",
    [
        # 500s should be retried
        ("https://example.com/internal-server-error/", 2, True, 2),
        ("https://example.com/internal-server-error/", 5, False, 3),
        # 429s should be retried
        ("https://example.com/rate-limit/", 2, True, 2),
        ("https://example.com/rate-limit/", 5, False, 3),
        # 404s shouldn't be retried
        ("https://example.com/not-found/", 3, True, 1),
    ],
)
def test_retry(url, max_retries, expect_failure, expect_requests):
    server = BrokenServer("example.com")
    urlopen = create_opener(server).open
    sleep_time = []
    dont_sleep = lambda t: sleep_time.append(t)  # keep track of sleep times

    try:
        response = default_retry(urlopen, retries=max_retries, sleep=dont_sleep)(url)
    except urllib.error.HTTPError as e:
        if not expect_failure:
            assert False, f"Unexpected HTTPError: {e}"
    else:
        if expect_failure:
            assert False, "Expected HTTPError, but none was raised"
        assert response.status == 200

    assert len(server.requests) == expect_requests
    assert sleep_time == [2**i for i in range(expect_requests - 1)]


def test_list_tags():
    # Follows a relatively new rewording of the OCI distribution spec, which is not yet tagged.
    # https://github.com/opencontainers/distribution-spec/commit/2ed79d930ecec11dd755dc8190409a3b10f01ca9
    N = 20
    urlopen = create_opener(InMemoryOCIRegistry("example.com", tags_per_page=5)).open
    image = ImageReference.from_string("example.com/image")
    to_tag = lambda i: f"tag-{i:02}"

    # Create N tags in arbitrary order
    _tags_to_create = [to_tag(i) for i in range(N)]
    random.shuffle(_tags_to_create)
    for tag in _tags_to_create:
        upload_manifest(image.with_tag(tag), default_manifest(), tag=True, _urlopen=urlopen)

    # list_tags should return all tags from all pages in order
    tags = list_tags(image, urlopen)
    assert len(tags) == N
    assert [to_tag(i) for i in range(N)] == tags

    # Test a single request, which should give the first 5 tags
    assert json.loads(urlopen(image.tags_url()).read())["tags"] == [to_tag(i) for i in range(5)]

    # Test response at an offset, which should exclude the `last` tag.
    assert json.loads(urlopen(image.tags_url() + f"?last={to_tag(N - 3)}").read())["tags"] == [
        to_tag(i) for i in range(N - 2, N)
    ]
