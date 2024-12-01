# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import os
import posixpath
import re
import urllib.parse
import urllib.request
from typing import Optional

from spack.util.path import sanitize_filename


def validate_scheme(scheme):
    """Returns true if the URL scheme is generally known to Spack. This function
    helps mostly in validation of paths vs urls, as Windows paths such as
    C:/x/y/z (with backward not forward slash) may parse as a URL with scheme
    C and path /x/y/z."""
    return scheme in ("file", "http", "https", "ftp", "s3", "gs", "ssh", "git")


def local_file_path(url):
    """Get a local file path from a url.

    If url is a file:// URL, return the absolute path to the local
    file or directory referenced by it.  Otherwise, return None.
    """
    if isinstance(url, str):
        url = urllib.parse.urlparse(url)

    if url.scheme == "file":
        return urllib.request.url2pathname(url.path)

    return None


def path_to_file_url(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return urllib.parse.urljoin("file:", urllib.request.pathname2url(path))


def file_url_string_to_path(url):
    return urllib.request.url2pathname(urllib.parse.urlparse(url).path)


def is_path_instead_of_url(path_or_url):
    """Historically some config files and spack commands used paths
    where urls should be used. This utility can be used to validate
    and promote paths to urls."""
    return not validate_scheme(urllib.parse.urlparse(path_or_url).scheme)


def format(parsed_url):
    """Format a URL string

    Returns a canonicalized format of the given URL as a string.
    """
    if isinstance(parsed_url, str):
        parsed_url = urllib.parse.urlparse(parsed_url)

    return parsed_url.geturl()


def join(base: str, *components: str, resolve_href: bool = False, **kwargs) -> str:
    """Convenience wrapper around ``urllib.parse.urljoin``, with a few differences:
    1. By default resolve_href=False, which makes the function like os.path.join: for example
    https://example.com/a/b + c/d = https://example.com/a/b/c/d. If resolve_href=True, the
    behavior is how a browser would resolve the URL: https://example.com/a/c/d.
    2. s3://, gs://, oci:// URLs are joined like http:// URLs.
    3. It accepts multiple components for convenience. Note that components[1:] are treated as
    literal path components and appended to components[0] separated by slashes."""
    # Ensure a trailing slash in the path component of the base URL to get os.path.join-like
    # behavior instead of web browser behavior.
    if not resolve_href:
        parsed = urllib.parse.urlparse(base)
        if not parsed.path.endswith("/"):
            base = parsed._replace(path=f"{parsed.path}/").geturl()
    uses_netloc = urllib.parse.uses_netloc
    uses_relative = urllib.parse.uses_relative
    try:
        # NOTE: we temporarily modify urllib internals so s3 and gs schemes are treated like http.
        # This is non-portable, and may be forward incompatible with future cpython versions.
        urllib.parse.uses_netloc = [*uses_netloc, "s3", "gs", "oci"]
        urllib.parse.uses_relative = [*uses_relative, "s3", "gs", "oci"]
        return urllib.parse.urljoin(base, "/".join(components), **kwargs)
    finally:
        urllib.parse.uses_netloc = uses_netloc
        urllib.parse.uses_relative = uses_relative


def default_download_filename(url: str) -> str:
    """This method computes a default file name for a given URL.
    Note that it makes no request, so this is not the same as the
    option curl -O, which uses the remote file name from the response
    header."""
    parsed_url = urllib.parse.urlparse(url)
    # Only use the last path component + params + query + fragment
    name = urllib.parse.urlunparse(
        parsed_url._replace(scheme="", netloc="", path=posixpath.basename(parsed_url.path))
    )
    valid_name = sanitize_filename(name)

    # Don't download to hidden files please
    if valid_name[0] == ".":
        valid_name = "_" + valid_name[1:]

    return valid_name


def parse_link_rel_next(link_value: str) -> Optional[str]:
    """Return the next link from a Link header value, if any."""

    # Relaxed version of RFC5988
    uri = re.compile(r"\s*<([^>]+)>\s*")
    param_key = r"[^;=\s]+"
    quoted_string = r"\"([^\"]+)\""
    unquoted_param_value = r"([^;,\s]+)"
    param = re.compile(rf";\s*({param_key})\s*=\s*(?:{quoted_string}|{unquoted_param_value})\s*")

    data = link_value

    # Parse a list of <url>; key=value; key=value, <url>; key=value; key=value, ... links.
    while True:
        uri_match = re.match(uri, data)
        if not uri_match:
            break
        uri_reference = uri_match.group(1)
        data = data[uri_match.end() :]

        # Parse parameter list
        while True:
            param_match = re.match(param, data)
            if not param_match:
                break
            key, quoted_value, unquoted_value = param_match.groups()
            value = quoted_value or unquoted_value
            data = data[param_match.end() :]

            if key == "rel" and value == "next":
                return uri_reference

        if not data.startswith(","):
            break

        data = data[1:]

    return None
