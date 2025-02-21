# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import os.path
import shutil
import tempfile
import urllib.parse
import urllib.request
from typing import Callable, Optional

import llnl.util.tty as tty
from llnl.util.filesystem import copy, join_path, mkdirp

import spack.util.crypto
from spack.util.path import canonicalize_path
from spack.util.url import validate_scheme


def raw_github_gitlab_url(url: str) -> str:
    """Transform a github URL to the raw form to avoid undesirable html.

    Args:
        url: url to be converted to raw form

    Returns:
        Raw github/gitlab url or the original url
    """
    # Note we rely on GitHub to redirect the 'raw' URL returned here to the
    # actual URL under https://raw.githubusercontent.com/ with '/blob'
    # removed and or, '/blame' if needed.
    if "github" in url or "gitlab" in url:
        return url.replace("/blob/", "/raw/")

    return url


def fetch_remote_text_file(url: str, dest_dir: str) -> str:
    """Retrieve the text file from the url into the destination directory.

    Arguments:
        url: URL for the remote text file
        dest_dir: destination directory in which to stage the file locally

    Returns:
        Path to the fetched file

    Raises:
        ValueError: if there are missing required arguments
    """
    from spack.util.web import fetch_url_text  # circular import

    if not url:
        raise ValueError("Cannot retrieve the remote file without the URL")

    raw_url = raw_github_gitlab_url(url)
    tty.debug(f"Fetching file from {raw_url} into {dest_dir}")

    return fetch_url_text(raw_url, dest_dir=dest_dir)


def local_path(raw_path: str, sha256: str, make_dest: Optional[Callable[[], str]] = None) -> str:
    """Determine the actual path and, if remote, stage its contents locally.

    Args:
        raw_path: raw path with possible variables needing substitution
        sha256: the expected sha256 for the file
        make_dest: function to create a stage for remote files, if needed (e.g., `mkdtemp`)

    Returns: resolved, normalized local path or None

    Raises:
        ValueError: missing or mismatched arguments, unsupported URL scheme
    """
    if not raw_path:
        raise ValueError("path argument is required to cache remote files")

    # Allow paths (and URLs) to contain spack config/environment variables,
    # etc.
    path = canonicalize_path(raw_path)
    url = urllib.parse.urlparse(path)

    # Path isn't remote so return absolute, normalized path with substitutions.
    if url.scheme in ["", "file"]:
        return path

    # If scheme is not valid, path is not a url
    # of a type Spack is generally aware
    if validate_scheme(url.scheme):
        # Fetch files from supported URL schemes.
        if url.scheme in ("http", "https", "ftp"):
            if make_dest is None:
                raise ValueError("Requires the destination argument to cache remote files")

            # Stage the remote configuration file
            tmpdir = tempfile.mkdtemp()
            try:
                staged_path = fetch_remote_text_file(path, tmpdir)

                # Ensure the sha256 is expected.
                checksum = spack.util.crypto.checksum(hashlib.sha256, staged_path)
                if sha256 and checksum != sha256:
                    raise ValueError(
                        f"Actual sha256 ('{checksum}') does not match expected ('{sha256}')"
                    )

                # Help the user by reporting the required checksum.
                if not sha256:
                    raise ValueError(f"Requires sha256 ('{checksum}') to cache remote files.")

                # Copy the file to the destination directory
                dest_dir = join_path(make_dest(), checksum)
                if not os.path.exists(dest_dir):
                    mkdirp(dest_dir)

                cache_path = join_path(dest_dir, os.path.basename(staged_path))
                copy(staged_path, cache_path)
                tty.debug(f"Cached {raw_path} in {cache_path}")

                # Stash the associated URL to aid with debugging
                with open(join_path(dest_dir, "source_url.txt"), "w", encoding="utf-8") as f:
                    f.write(f"{raw_path}\n")

                return cache_path

            except ValueError as err:
                tty.warn(f"Unable to cache {raw_path}: {str(err)}")
                raise

            finally:
                shutil.rmtree(tmpdir)

        raise ValueError(f"Unsupported URL scheme ({url.scheme}) in {raw_path}")

    else:
        raise ValueError(f"Invalid URL scheme ({url.scheme}) in {raw_path}")
