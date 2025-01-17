# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp, touchp

import spack.config
import spack.util.web

github_url = "https://github.com/fake/fake/{0}/develop"
gitlab_url = "https://gitlab.fake.io/user/repo/-/blob/config/defaults"


@pytest.fixture(scope="function")
def mock_collect_urls(mock_config_data, monkeypatch):
    """Mock the collection of URLs to avoid mocking spider."""

    _, config_files = mock_config_data

    def _collect(base_url, extension):
        if not base_url:
            return []

        ext = os.path.splitext(base_url)[1]
        if ext:
            return [base_url] if ext == ".yaml" else []

        return [join_path(base_url, f) for f in config_files]

    monkeypatch.setattr(spack.util.web, "collect_urls", _collect)

    yield


@pytest.mark.parametrize(
    "url,isfile",
    [
        (github_url.format("tree"), False),
        (f"{github_url.format('blob')}/README.md", True),
        (f"{github_url.format('blob')}/etc/fake/defaults/packages.yaml", True),
        (gitlab_url, False),
        (None, False),
    ],
)
def test_collect_urls(mutable_empty_config, mock_spider_configs, url, isfile):
    with spack.config.override("config:url_fetch_method", "curl"):
        urls = spack.util.web.collect_urls(url, ".yaml")
        if url:
            if isfile:
                expected = 1 if url.endswith(".yaml") else 0
                assert len(urls) == expected
            else:
                # Expect multiple configuration files for a "directory"
                assert len(urls) > 1
        else:
            assert not urls


@pytest.mark.parametrize(
    "url,isfile,fail",
    [
        (github_url.format("tree"), False, False),
        (gitlab_url, False, False),
        (f"{github_url.format('blob')}/README.md", True, True),
        (f"{gitlab_url}/compilers.yaml", True, False),
        (None, False, True),
    ],
)
def test_fetch_remote_configs(
    tmpdir, mutable_empty_config, mock_collect_urls, mock_curl_configs, url, isfile, fail
):
    def _has_content(filename):
        # The first element of all configuration files for this test happen to
        # be the basename of the file so this check leverages that feature. If
        # that changes, then this check will need to change accordingly.
        element = f"{os.path.splitext(os.path.basename(filename))[0]}:"
        with open(filename, "r", encoding="utf-8") as fd:
            for line in fd:
                if element in line:
                    return True
        tty.debug(f"Expected {element} in '{filename}'")
        return False

    dest_dir = join_path(tmpdir.strpath, "cache")
    if fail:
        msg = "Cannot retrieve"
        error = ValueError if url is None else spack.util.web.RemoteFileError
        with spack.config.override("config:url_fetch_method", "curl"):
            with pytest.raises(error, match=msg):
                spack.util.web.fetch_remote_files(url, ".yaml", dest_dir)
    else:
        with spack.config.override("config:url_fetch_method", "curl"):
            path = spack.util.web.fetch_remote_files(url, ".yaml", dest_dir)
            assert os.path.exists(path)
            if isfile and os.path.isfile(path):
                # Ensure correct file is "fetched"
                assert os.path.basename(path) == os.path.basename(url)
                # Ensure contents of the file has expected config element
                assert _has_content(path)
            else:
                for filename in os.listdir(path):
                    assert _has_content(join_path(path, filename))


def test_fetch_remote_configs_skip(
    tmpdir, mutable_empty_config, mock_collect_urls, mock_curl_configs
):
    """Ensure skip fetching remote config file if it already exists."""

    dest_dir = join_path(tmpdir.strpath, "cache")
    filename = "compilers.yaml"
    url = f"{gitlab_url}/{filename}"

    # Create the stage directory with an empty configuration file
    dest_path = spack.util.web.local_cache_path(dest_dir, url)

    mkdirp(os.path.dirname(dest_path))
    join_path(dest_path, filename)
    touchp(dest_path)

    with spack.config.override("config:url_fetch_method", "curl"):
        cached_path = spack.util.web.fetch_remote_files(url, filename, dest_dir, True)
        # The resulting path must be a file under the destination directory
        assert cached_path.startswith(dest_dir)
        assert os.path.isfile(cached_path)

        # And the file must be empty (i.e., not replaced)
        with open(cached_path, "r", encoding="utf-8") as fd:
            lines = fd.readlines()
            assert not lines
