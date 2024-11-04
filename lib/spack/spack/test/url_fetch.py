# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import filecmp
import os
import sys
import urllib.error

import pytest

import llnl.util.tty as tty
from llnl.util.filesystem import is_exe, working_dir

import spack.config
import spack.error
import spack.fetch_strategy as fs
import spack.url
import spack.util.crypto as crypto
import spack.util.executable
import spack.util.web as web_util
import spack.version
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which


@pytest.fixture
def missing_curl(monkeypatch):
    def require_curl():
        raise spack.error.FetchError("curl is required but not found")

    monkeypatch.setattr(web_util, "require_curl", require_curl)


@pytest.fixture(params=list(crypto.hashes.keys()))
def checksum_type(request):
    return request.param


@pytest.fixture
def pkg_factory():
    Pkg = collections.namedtuple(
        "Pkg",
        [
            "url_for_version",
            "all_urls_for_version",
            "find_valid_url_for_version",
            "urls",
            "url",
            "versions",
            "fetch_options",
        ],
    )

    def factory(url, urls, fetch_options={}):
        def fn(v):
            main_url = url or urls[0]
            return spack.url.substitute_version(main_url, v)

        def fn_urls(v):
            urls_loc = urls or [url]
            return [spack.url.substitute_version(u, v) for u in urls_loc]

        return Pkg(
            find_valid_url_for_version=fn,
            url_for_version=fn,
            all_urls_for_version=fn_urls,
            url=url,
            urls=(urls,),
            versions=collections.defaultdict(dict),
            fetch_options=fetch_options,
        )

    return factory


@pytest.mark.parametrize("method", ["curl", "urllib"])
def test_urlfetchstrategy_bad_url(tmp_path, mutable_config, method):
    """Ensure fetch with bad URL fails as expected."""
    mutable_config.set("config:url_fetch_method", method)
    fetcher = fs.URLFetchStrategy(url=(tmp_path / "does-not-exist").as_uri())

    with Stage(fetcher, path=str(tmp_path / "stage")):
        with pytest.raises(fs.FailedDownloadError) as exc:
            fetcher.fetch()

    assert len(exc.value.exceptions) == 1
    exception = exc.value.exceptions[0]

    if method == "curl":
        assert isinstance(exception, spack.error.FetchError)
        assert "Curl failed with error 37" in str(exception)  # FILE_COULDNT_READ_FILE
    elif method == "urllib":
        assert isinstance(exception, urllib.error.URLError)
        assert isinstance(exception.reason, FileNotFoundError)


def test_fetch_options(tmp_path, mock_archive):
    with spack.config.override("config:url_fetch_method", "curl"):
        fetcher = fs.URLFetchStrategy(
            url=mock_archive.url, fetch_options={"cookie": "True", "timeout": 10}
        )

        with Stage(fetcher, path=str(tmp_path)):
            assert fetcher.archive_file is None
            fetcher.fetch()
            assert filecmp.cmp(fetcher.archive_file, mock_archive.archive_file)


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_archive_file_errors(tmp_path, mutable_config, mock_archive, _fetch_method):
    """Ensure FetchStrategy commands may only be used as intended"""
    with spack.config.override("config:url_fetch_method", _fetch_method):
        fetcher = fs.URLFetchStrategy(url=mock_archive.url)
        with Stage(fetcher, path=str(tmp_path)) as stage:
            assert fetcher.archive_file is None
            with pytest.raises(fs.NoArchiveFileError):
                fetcher.archive(str(tmp_path))
            with pytest.raises(fs.NoArchiveFileError):
                fetcher.expand()
            with pytest.raises(fs.NoArchiveFileError):
                fetcher.reset()
            stage.fetch()
            with pytest.raises(fs.NoDigestError):
                fetcher.check()
            assert filecmp.cmp(fetcher.archive_file, mock_archive.archive_file)


files = [(".tar.gz", "z"), (".tgz", "z")]
if sys.platform != "win32":
    files += [(".tar.bz2", "j"), (".tbz2", "j"), (".tar.xz", "J"), (".txz", "J")]


@pytest.mark.parametrize("secure", [True, False])
@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
@pytest.mark.parametrize("mock_archive", files, indirect=True)
def test_fetch(
    mock_archive,
    secure,
    _fetch_method,
    checksum_type,
    default_mock_concretization,
    mutable_mock_repo,
):
    """Fetch an archive and make sure we can checksum it."""
    algo = crypto.hash_fun_for_algo(checksum_type)()
    with open(mock_archive.archive_file, "rb") as f:
        algo.update(f.read())
    checksum = algo.hexdigest()

    # Get a spec and tweak the test package with new checksum params
    s = default_mock_concretization("url-test")
    s.package.url = mock_archive.url
    s.package.versions[spack.version.Version("test")] = {
        checksum_type: checksum,
        "url": s.package.url,
    }

    # Enter the stage directory and check some properties
    with s.package.stage:
        with spack.config.override("config:verify_ssl", secure):
            with spack.config.override("config:url_fetch_method", _fetch_method):
                s.package.do_stage()
        with working_dir(s.package.stage.source_path):
            assert os.path.exists("configure")
            assert is_exe("configure")

            with open("configure") as f:
                contents = f.read()
            assert contents.startswith("#!/bin/sh")
            assert "echo Building..." in contents


@pytest.mark.parametrize(
    "spec,url,digest",
    [
        ("url-list-test @=0.0.0", "foo-0.0.0.tar.gz", "00000000000000000000000000000000"),
        ("url-list-test @=1.0.0", "foo-1.0.0.tar.gz", "00000000000000000000000000000100"),
        ("url-list-test @=3.0", "foo-3.0.tar.gz", "00000000000000000000000000000030"),
        ("url-list-test @=4.5", "foo-4.5.tar.gz", "00000000000000000000000000000450"),
        ("url-list-test @=2.0.0b2", "foo-2.0.0b2.tar.gz", "000000000000000000000000000200b2"),
        ("url-list-test @=3.0a1", "foo-3.0a1.tar.gz", "000000000000000000000000000030a1"),
        ("url-list-test @=4.5-rc5", "foo-4.5-rc5.tar.gz", "000000000000000000000000000045c5"),
    ],
)
@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_from_list_url(mock_packages, config, spec, url, digest, _fetch_method):
    """
    Test URLs in the url-list-test package, which means they should
    have checksums in the package.
    """
    with spack.config.override("config:url_fetch_method", _fetch_method):
        s = Spec(spec).concretized()
        fetch_strategy = fs.from_list_url(s.package)
        assert isinstance(fetch_strategy, fs.URLFetchStrategy)
        assert os.path.basename(fetch_strategy.url) == url
        assert fetch_strategy.digest == digest
        assert fetch_strategy.extra_options == {}
        s.package.fetch_options = {"timeout": 60}
        fetch_strategy = fs.from_list_url(s.package)
        assert fetch_strategy.extra_options == {"timeout": 60}


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
@pytest.mark.parametrize(
    "requested_version,tarball,digest",
    [
        # These versions are in the web data path (test/data/web/4.html), but not in the
        # url-list-test package. We expect Spack to generate a URL with the new version.
        ("=4.5.0", "foo-4.5.0.tar.gz", None),
        ("=2.0.0", "foo-2.0.0.tar.gz", None),
    ],
)
def test_new_version_from_list_url(
    mock_packages, config, _fetch_method, requested_version, tarball, digest
):
    """Test non-specific URLs from the url-list-test package."""
    with spack.config.override("config:url_fetch_method", _fetch_method):
        s = Spec(f"url-list-test @{requested_version}").concretized()
        fetch_strategy = fs.from_list_url(s.package)

        assert isinstance(fetch_strategy, fs.URLFetchStrategy)
        assert os.path.basename(fetch_strategy.url) == tarball
        assert fetch_strategy.digest == digest
        assert fetch_strategy.extra_options == {}
        s.package.fetch_options = {"timeout": 60}
        fetch_strategy = fs.from_list_url(s.package)
        assert fetch_strategy.extra_options == {"timeout": 60}


def test_nosource_from_list_url(mock_packages, config):
    """This test confirms BundlePackages do not have list url."""
    s = Spec("nosource").concretized()
    fetch_strategy = fs.from_list_url(s.package)
    assert fetch_strategy is None


def test_hash_detection(checksum_type):
    algo = crypto.hash_fun_for_algo(checksum_type)()
    h = "f" * (algo.digest_size * 2)  # hex -> bytes
    checker = crypto.Checker(h)
    assert checker.hash_name == checksum_type


def test_unknown_hash(checksum_type):
    with pytest.raises(ValueError):
        crypto.Checker("a")


@pytest.mark.skipif(which("curl") is None, reason="Urllib does not have built-in status bar")
def test_url_with_status_bar(tmpdir, mock_archive, monkeypatch, capfd):
    """Ensure fetch with status bar option succeeds."""

    def is_true():
        return True

    testpath = str(tmpdir)

    monkeypatch.setattr(sys.stdout, "isatty", is_true)
    monkeypatch.setattr(tty, "msg_enabled", is_true)
    with spack.config.override("config:url_fetch_method", "curl"):
        fetcher = fs.URLFetchStrategy(url=mock_archive.url)
        with Stage(fetcher, path=testpath) as stage:
            assert fetcher.archive_file is None
            stage.fetch()

        status = capfd.readouterr()[1]
        assert "##### 100" in status


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_url_extra_fetch(tmp_path, mutable_config, mock_archive, _fetch_method):
    """Ensure a fetch after downloading is effectively a no-op."""
    mutable_config.set("config:url_fetch_method", _fetch_method)
    fetcher = fs.URLFetchStrategy(url=mock_archive.url)
    with Stage(fetcher, path=str(tmp_path)) as stage:
        assert fetcher.archive_file is None
        stage.fetch()
        assert filecmp.cmp(fetcher.archive_file, mock_archive.archive_file)
        fetcher.fetch()


@pytest.mark.parametrize(
    "url,urls,version,expected",
    [
        (
            None,
            [
                "https://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz",
                "https://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz",
            ],
            "2.62",
            [
                "https://ftpmirror.gnu.org/autoconf/autoconf-2.62.tar.gz",
                "https://ftp.gnu.org/gnu/autoconf/autoconf-2.62.tar.gz",
            ],
        )
    ],
)
@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_candidate_urls(pkg_factory, url, urls, version, expected, _fetch_method):
    """Tests that candidate urls include mirrors and that they go through
    pattern matching and substitution for versions.
    """
    with spack.config.override("config:url_fetch_method", _fetch_method):
        pkg = pkg_factory(url, urls)
        f = fs._from_merged_attrs(fs.URLFetchStrategy, pkg, version)
        assert f.candidate_urls == expected
        assert f.extra_options == {}
        pkg = pkg_factory(url, urls, fetch_options={"timeout": 60})
        f = fs._from_merged_attrs(fs.URLFetchStrategy, pkg, version)
        assert f.extra_options == {"timeout": 60}


@pytest.mark.regression("19673")
def test_missing_curl(tmp_path, missing_curl, mutable_config, monkeypatch):
    """Ensure a fetch involving missing curl package reports the error."""
    mutable_config.set("config:url_fetch_method", "curl")
    fetcher = fs.URLFetchStrategy(url="http://example.com/file.tar.gz")
    with pytest.raises(spack.error.FetchError, match="curl is required but not found"):
        with Stage(fetcher, path=str(tmp_path)) as stage:
            stage.fetch()


def test_url_fetch_text_without_url():
    with pytest.raises(spack.error.FetchError, match="URL is required"):
        web_util.fetch_url_text(None)


def test_url_fetch_text_curl_failures(mutable_config, missing_curl, monkeypatch):
    """Check fetch_url_text if URL's curl is missing."""
    mutable_config.set("config:url_fetch_method", "curl")
    with pytest.raises(spack.error.FetchError, match="curl is required but not found"):
        web_util.fetch_url_text("https://example.com/")


def test_url_check_curl_errors():
    """Check that standard curl error returncodes raise expected errors."""
    # Check returncode 22 (i.e., 404)
    with pytest.raises(spack.error.FetchError, match="not found"):
        web_util.check_curl_code(22)

    # Check returncode 60 (certificate error)
    with pytest.raises(spack.error.FetchError, match="invalid certificate"):
        web_util.check_curl_code(60)


def test_url_missing_curl(mutable_config, missing_curl, monkeypatch):
    """Check url_exists failures if URL's curl is missing."""
    mutable_config.set("config:url_fetch_method", "curl")
    with pytest.raises(spack.error.FetchError, match="curl is required but not found"):
        web_util.url_exists("https://example.com/")


def test_url_fetch_text_urllib_bad_returncode(mutable_config, monkeypatch):
    class response:
        def getcode(self):
            return 404

    def _read_from_url(*args, **kwargs):
        return None, None, response()

    monkeypatch.setattr(web_util, "read_from_url", _read_from_url)
    mutable_config.set("config:url_fetch_method", "urllib")

    with pytest.raises(spack.error.FetchError, match="failed with error code"):
        web_util.fetch_url_text("https://example.com/")


def test_url_fetch_text_urllib_web_error(mutable_config, monkeypatch):
    def _raise_web_error(*args, **kwargs):
        raise web_util.SpackWebError("bad url")

    monkeypatch.setattr(web_util, "read_from_url", _raise_web_error)
    mutable_config.set("config:url_fetch_method", "urllib")

    with pytest.raises(spack.error.FetchError, match="fetch failed to verify"):
        web_util.fetch_url_text("https://example.com/")
