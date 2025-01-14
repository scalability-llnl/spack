# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from io import BufferedReader, BytesIO, IOBase
from typing import Any, Dict, Tuple

import spack.config

#: Map (mirror name, method) tuples to s3 client instances.
s3_client_cache: Dict[Tuple[str, str], Any] = dict()


def get_s3_session(url, method="fetch"):
    # import boto and friends as late as possible.  We don't want to require boto as a
    # dependency unless the user actually wants to access S3 mirrors.
    from boto3 import Session
    from botocore import UNSIGNED
    from botocore.client import Config
    from botocore.exceptions import ClientError

    # Circular dependency
    from spack.mirrors.mirror import MirrorCollection

    global s3_client_cache

    # Parse the URL if not already done.
    if not isinstance(url, urllib.parse.ParseResult):
        url = urllib.parse.urlparse(url)
    url_str = url.geturl()

    def get_mirror_url(mirror):
        return mirror.fetch_url if method == "fetch" else mirror.push_url

    # Get all configured mirrors that could match.
    all_mirrors = MirrorCollection()
    mirrors = [
        (name, mirror)
        for name, mirror in all_mirrors.items()
        if url_str.startswith(get_mirror_url(mirror))
    ]

    if not mirrors:
        name, mirror = None, {}
    else:
        # In case we have more than one mirror, we pick the longest matching url.
        # The heuristic being that it's more specific, and you can have different
        # credentials for a sub-bucket (if that is a thing).
        name, mirror = max(
            mirrors, key=lambda name_and_mirror: len(get_mirror_url(name_and_mirror[1]))
        )

    key = (name, method)

    # Did we already create a client for this? Then return it.
    if key in s3_client_cache:
        return s3_client_cache[key]

    # Otherwise, create it.
    s3_connection, s3_client_args = get_mirror_s3_connection_info(mirror, method)

    session = Session(**s3_connection)
    # if no access credentials provided above, then access anonymously
    if not session.get_credentials():
        s3_client_args["config"] = Config(signature_version=UNSIGNED)

    client = session.client("s3", **s3_client_args)
    client.ClientError = ClientError

    # Cache the client.
    s3_client_cache[key] = client
    return client


def _parse_s3_endpoint_url(endpoint_url):
    if not urllib.parse.urlparse(endpoint_url, scheme="").scheme:
        endpoint_url = "://".join(("https", endpoint_url))

    return endpoint_url


def get_mirror_s3_connection_info(mirror, method):
    """Create s3 config for session/client from a Mirror instance (or just set defaults
    when no mirror is given.)"""
    from spack.mirrors.mirror import Mirror

    s3_connection = {}
    s3_client_args = {"use_ssl": spack.config.get("config:verify_ssl")}

    # access token
    if isinstance(mirror, Mirror):
        credentials = mirror.get_credentials(method)
        if credentials:
            if "access_token" in credentials:
                s3_connection["aws_session_token"] = credentials["access_token"]

            if "access_pair" in credentials:
                s3_connection["aws_access_key_id"] = credentials["access_pair"][0]
                s3_connection["aws_secret_access_key"] = credentials["access_pair"][1]

            if "profile" in credentials:
                s3_connection["profile_name"] = credentials["profile"]

        # endpoint url
        endpoint_url = mirror.get_endpoint_url(method) or os.environ.get("S3_ENDPOINT_URL")
    else:
        endpoint_url = os.environ.get("S3_ENDPOINT_URL")

    if endpoint_url:
        s3_client_args["endpoint_url"] = _parse_s3_endpoint_url(endpoint_url)

    return s3_connection, s3_client_args


# NOTE(opadron): Workaround issue in boto where its StreamingBody
# implementation is missing several APIs expected from IOBase.  These missing
# APIs prevent the streams returned by boto from being passed as-are along to
# urllib.
#
# https://github.com/boto/botocore/issues/879
# https://github.com/python/cpython/pull/3249
class WrapStream(BufferedReader):
    def __init__(self, raw):
        # In botocore >=1.23.47, StreamingBody inherits from IOBase, so we
        # only add missing attributes in older versions.
        # https://github.com/boto/botocore/commit/a624815eabac50442ed7404f3c4f2664cd0aa784
        if not isinstance(raw, IOBase):
            raw.readable = lambda: True
            raw.writable = lambda: False
            raw.seekable = lambda: False
            raw.closed = False
            raw.flush = lambda: None
        super().__init__(raw)

    def detach(self):
        self.raw = None

    def read(self, *args, **kwargs):
        return self.raw.read(*args, **kwargs)

    def __getattr__(self, key):
        return getattr(self.raw, key)


def _s3_open(url, method="GET"):
    parsed = urllib.parse.urlparse(url)
    s3 = get_s3_session(url, method="fetch")

    bucket = parsed.netloc
    key = parsed.path

    if key.startswith("/"):
        key = key[1:]

    if method not in ("GET", "HEAD"):
        raise urllib.error.URLError(
            "Only GET and HEAD verbs are currently supported for the s3:// scheme"
        )

    try:
        if method == "GET":
            obj = s3.get_object(Bucket=bucket, Key=key)
            # NOTE(opadron): Apply workaround here (see above)
            stream = WrapStream(obj["Body"])
        elif method == "HEAD":
            obj = s3.head_object(Bucket=bucket, Key=key)
            stream = BytesIO()
    except s3.ClientError as e:
        raise urllib.error.URLError(e) from e

    headers = obj["ResponseMetadata"]["HTTPHeaders"]

    return url, headers, stream


class UrllibS3Handler(urllib.request.BaseHandler):
    def s3_open(self, req):
        orig_url = req.get_full_url()
        url, headers, stream = _s3_open(orig_url, method=req.get_method())
        return urllib.response.addinfourl(stream, headers, url)
