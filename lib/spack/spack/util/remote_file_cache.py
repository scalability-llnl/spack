# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

import llnl.util.tty as tty
from llnl.util.filesystem import join_path

import spack.error
import spack.util.web as web_util


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


def collect_urls(base_url: str, extension: str) -> list:
    """Return a list of URLs with the provided extension.

    Arguments:
        base_url: URL for a configuration (yaml) file or a directory
            containing yaml file(s)
        extension: desired file extension

    Returns:
        List of file(s) or empty list if none
    """

    if not base_url:
        return []

    if extension and base_url.endswith(extension):
        return [base_url]

    # Collect relevant URLs within the base_url "directory".
    _, links = web_util.spider(base_url, 0)
    return [link for link in links if link.endswith(extension)]


def local_cache_path(dest_dir: str, url: str) -> str:
    """Derive the local cache path from the destination directory and url.

    Args:
        url: URL for the file or a directory containing the desired file(s)
        dest_dir: destination directory in which to cache the file(s) locally

    Returns: path to the local path equivalent of the url
    """
    return join_path(dest_dir, url.replace(":/", ""))


def fetch_remote_files(url: str, extension: str, dest_dir: str, skip_existing: bool = True) -> str:
    """Retrieve file(s) with the provided extension from the specified URL.

    Arguments:
        url: URL for the file or a directory containing the desired file(s)
        extension: desired extension of retrieved file(s) (e.g., ".yaml")
        dest_dir: destination directory in which to cache the files locally
        skip_existing: Skip files that already exist in dest_dir if
            ``True``; otherwise, replace those files

    Returns:
        Path to the corresponding file if URL is or contains a
        single file and it is the only file in the destination directory or
        the root (dest_dir) directory if multiple configuration files exist
        or are retrieved.

    Raises:
        spack.error.RemoteFileError: if there is a problem fetching remote file(s)
        ValueError: if the URL is not provided
    """

    def _fetch_file(url, dest):
        raw = raw_github_gitlab_url(url)
        tty.debug(f"Reading config from url {raw} into {dest}")
        return web_util.fetch_url_text(raw, dest_dir=dest)

    if not url:
        raise ValueError(f"Cannot retrieve a remote {extension} file without the URL")

    # Return the local path to the cached file OR to the directory containing
    # the cached files.
    links = collect_urls(url, extension)

    paths = []
    for file_url in links:
        local_path = local_cache_path(dest_dir, file_url)
        if skip_existing and os.path.isfile(local_path):
            tty.warn(
                f"Will not (re-)fetch file from {file_url} since it already "
                f"exists at {local_path}."
            )
            path = local_path
        else:
            path = _fetch_file(file_url, os.path.dirname(local_path))

        if path:
            paths.append(path)

    if paths:
        result = os.path.dirname(paths[0]) if len(paths) > 1 else paths[0]
        return result
        # return dest_dir if len(paths) > 1 else paths[0]

    raise spack.error.RemoteFileError(f"Cannot retrieve remote ({extension}) file(s) from {url}")
