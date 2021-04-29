# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
import pytest
import sys

from llnl.util.filesystem import working_dir, is_exe
import llnl.util.tty as tty

import spack.repo
import spack.config
import spack.fetch_strategy as fs
from spack.spec import Spec
from spack.stage import Stage
from spack.version import ver
import spack.util.crypto as crypto
import spack.util.executable
from spack.util.executable import which


@pytest.fixture(params=list(crypto.hashes.keys()))
def checksum_type(request):
    return request.param


@pytest.fixture
def pkg_factory():
    Pkg = collections.namedtuple(
        'Pkg', ['url_for_version', 'urls', 'url', 'versions', 'fetch_options']
    )

    def factory(url, urls, fetch_options={}):

        def fn(v):
            main_url = url or urls[0]
            return spack.url.substitute_version(main_url, v)

        return Pkg(
            url_for_version=fn, url=url, urls=urls,
            versions=collections.defaultdict(dict),
            fetch_options=fetch_options
        )

    return factory


@pytest.mark.parametrize('use_curl', [True, False])
def test_urlfetchstrategy_sans_url(use_curl):
    """Ensure constructor with no URL fails."""
    with spack.config.override('config:use_curl', use_curl):
        with pytest.raises(ValueError):
            with fs.URLFetchStrategy(None):
                pass


@pytest.mark.parametrize('use_curl', [True, False])
def test_urlfetchstrategy_bad_url(tmpdir, use_curl):
    """Ensure fetch with bad URL fails as expected."""
    testpath = str(tmpdir)
    with spack.config.override('config:use_curl', use_curl):
        with pytest.raises(fs.FailedDownloadError):
            fetcher = fs.URLFetchStrategy(url='file:///does-not-exist')
            assert fetcher is not None

            with Stage(fetcher, path=testpath) as stage:
                assert stage is not None
                assert fetcher.archive_file is None
                fetcher.fetch()


def test_fetch_options(tmpdir, mock_archive):
    testpath = str(tmpdir)
    with spack.config.override('config:use_curl', True):
        fetcher = fs.URLFetchStrategy(url=mock_archive.url,
                                      fetch_options={'cookie': 'True',
                                                     'timeout': 10})
        assert fetcher is not None

        with Stage(fetcher, path=testpath) as stage:
            assert stage is not None
            assert fetcher.archive_file is None
            fetcher.fetch()


@pytest.mark.parametrize('use_curl', [True, False])
def test_archive_file_errors(tmpdir, mock_archive, use_curl):
    """Ensure FetchStrategy commands may only be used as intended"""
    testpath = str(tmpdir)
    with spack.config.override('config:use_curl', use_curl):
        fetcher = fs.URLFetchStrategy(url=mock_archive.url)
        assert fetcher is not None
        with pytest.raises(fs.FailedDownloadError):
            with Stage(fetcher, path=testpath) as stage:
                assert stage is not None
                assert fetcher.archive_file is None
                with pytest.raises(fs.NoArchiveFileError):
                    fetcher.archive(testpath)
                with pytest.raises(fs.NoArchiveFileError):
                    fetcher.expand()
                with pytest.raises(fs.NoArchiveFileError):
                    fetcher.reset()
                stage.fetch()
                with pytest.raises(fs.NoDigestError):
                    fetcher.check()
                assert fetcher.archive_file is not None
                fetcher._fetch_from_url('file:///does-not-exist')


@pytest.mark.parametrize('secure', [True, False])
@pytest.mark.parametrize('use_curl', [True, False])
@pytest.mark.parametrize('mock_archive',
                         [('.tar.gz', 'z'), ('.tgz', 'z'),
                          ('.tar.bz2', 'j'), ('.tbz2', 'j'),
                          ('.tar.xz', 'J'), ('.txz', 'J')],
                         indirect=True)
def test_fetch(
        mock_archive,
        secure,
        use_curl,
        checksum_type,
        config,
        mutable_mock_repo
):
    """Fetch an archive and make sure we can checksum it."""
    mock_archive.url
    mock_archive.path

    algo = crypto.hash_fun_for_algo(checksum_type)()
    with open(mock_archive.archive_file, 'rb') as f:
        algo.update(f.read())
    checksum = algo.hexdigest()

    # Get a spec and tweak the test package with new chcecksum params
    spec = Spec('url-test')
    spec.concretize()

    pkg = spack.repo.get('url-test')
    pkg.url = mock_archive.url
    pkg.versions[ver('test')] = {checksum_type: checksum, 'url': pkg.url}
    pkg.spec = spec

    # Enter the stage directory and check some properties
    with pkg.stage:
        with spack.config.override('config:verify_ssl', secure):
            with spack.config.override('config:use_curl', use_curl):
                pkg.do_stage()
        with working_dir(pkg.stage.source_path):
            assert os.path.exists('configure')
            assert is_exe('configure')

            with open('configure') as f:
                contents = f.read()
            assert contents.startswith('#!/bin/sh')
            assert 'echo Building...' in contents


@pytest.mark.parametrize('spec,url,digest', [
    ('url-list-test @0.0.0', 'foo-0.0.0.tar.gz', 'abc000'),
    ('url-list-test @1.0.0', 'foo-1.0.0.tar.gz', 'abc100'),
    ('url-list-test @3.0', 'foo-3.0.tar.gz', 'abc30'),
    ('url-list-test @4.5', 'foo-4.5.tar.gz', 'abc45'),
    ('url-list-test @2.0.0b2', 'foo-2.0.0b2.tar.gz', 'abc200b2'),
    ('url-list-test @3.0a1', 'foo-3.0a1.tar.gz', 'abc30a1'),
    ('url-list-test @4.5-rc5', 'foo-4.5-rc5.tar.gz', 'abc45rc5'),
])
@pytest.mark.parametrize('use_curl', [True, False])
def test_from_list_url(mock_packages, config, spec, url, digest, use_curl):
    """
    Test URLs in the url-list-test package, which means they should
    have checksums in the package.
    """
    with spack.config.override('config:use_curl', use_curl):
        specification = Spec(spec).concretized()
        pkg = spack.repo.get(specification)
        fetch_strategy = fs.from_list_url(pkg)
        assert isinstance(fetch_strategy, fs.URLFetchStrategy)
        assert os.path.basename(fetch_strategy.url) == url
        assert fetch_strategy.digest == digest
        assert fetch_strategy.extra_options == {}
        pkg.fetch_options = {'timeout': 60}
        fetch_strategy = fs.from_list_url(pkg)
        assert fetch_strategy.extra_options == {'timeout': 60}


@pytest.mark.parametrize('use_curl', [True, False])
def test_from_list_url_unspecified(mock_packages, config, use_curl):
    """Test non-specific URLs from the url-list-test package."""
    with spack.config.override('config:use_curl', use_curl):
        pkg = spack.repo.get('url-list-test')

        spec = Spec('url-list-test @2.0.0').concretized()
        pkg = spack.repo.get(spec)
        fetch_strategy = fs.from_list_url(pkg)
        assert isinstance(fetch_strategy, fs.URLFetchStrategy)
        assert os.path.basename(fetch_strategy.url) == 'foo-2.0.0.tar.gz'
        assert fetch_strategy.digest is None
        assert fetch_strategy.extra_options == {}
        pkg.fetch_options = {'timeout': 60}
        fetch_strategy = fs.from_list_url(pkg)
        assert fetch_strategy.extra_options == {'timeout': 60}


def test_nosource_from_list_url(mock_packages, config):
    """This test confirms BundlePackages do not have list url."""
    pkg = spack.repo.get('nosource')

    fetch_strategy = fs.from_list_url(pkg)
    assert fetch_strategy is None


def test_hash_detection(checksum_type):
    algo = crypto.hash_fun_for_algo(checksum_type)()
    h = 'f' * (algo.digest_size * 2)  # hex -> bytes
    checker = crypto.Checker(h)
    assert checker.hash_name == checksum_type


def test_unknown_hash(checksum_type):
    with pytest.raises(ValueError):
        crypto.Checker('a')


@pytest.mark.skipif(which('curl') is None,
                    reason='Urllib does not have built-in status bar')
def test_url_with_status_bar(tmpdir, mock_archive, monkeypatch, capfd):
    """Ensure fetch with status bar option succeeds."""
    def is_true():
        return True

    testpath = str(tmpdir)

    monkeypatch.setattr(sys.stdout, 'isatty', is_true)
    monkeypatch.setattr(tty, 'msg_enabled', is_true)
    with spack.config.override('config:use_curl', True):
        fetcher = fs.URLFetchStrategy(mock_archive.url)
        with Stage(fetcher, path=testpath) as stage:
            assert fetcher.archive_file is None
            stage.fetch()

        status = capfd.readouterr()[1]
        assert '##### 100' in status


@pytest.mark.parametrize('use_curl', [True, False])
def test_url_extra_fetch(tmpdir, mock_archive, use_curl):
    """Ensure a fetch after downloading is effectively a no-op."""
    with spack.config.override('config:use_curl', use_curl):
        testpath = str(tmpdir)
        fetcher = fs.URLFetchStrategy(mock_archive.url)
        with Stage(fetcher, path=testpath) as stage:
            assert fetcher.archive_file is None
            stage.fetch()
            assert fetcher.archive_file is not None
            fetcher.fetch()


@pytest.mark.parametrize('url,urls,version,expected', [
    (None,
     ['https://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz',
      'https://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz'],
     '2.62',
     ['https://ftpmirror.gnu.org/autoconf/autoconf-2.62.tar.gz',
      'https://ftp.gnu.org/gnu/autoconf/autoconf-2.62.tar.gz'])
])
@pytest.mark.parametrize('use_curl', [True, False])
def test_candidate_urls(pkg_factory, url, urls, version, expected, use_curl):
    """Tests that candidate urls include mirrors and that they go through
    pattern matching and substitution for versions.
    """
    with spack.config.override('config:use_curl', use_curl):
        pkg = pkg_factory(url, urls)
        f = fs._from_merged_attrs(fs.URLFetchStrategy, pkg, version)
        assert f.candidate_urls == expected
        assert f.extra_options == {}
        pkg = pkg_factory(url, urls, fetch_options={'timeout': 60})
        f = fs._from_merged_attrs(fs.URLFetchStrategy, pkg, version)
        assert f.extra_options == {'timeout': 60}


@pytest.mark.regression('19673')
def test_missing_curl(tmpdir, monkeypatch):
    """Ensure a fetch involving missing curl package reports the error."""
    err_fmt = 'No such command {0}'

    def _which(*args, **kwargs):
        err_msg = err_fmt.format(args[0])
        raise spack.util.executable.CommandNotFoundError(err_msg)

    # Patching the 'which' symbol imported by fetch_strategy works
    # since it is too late in import processing to patch the defining
    # (spack.util.executable) module's symbol.
    monkeypatch.setattr(fs, 'which', _which)

    testpath = str(tmpdir)
    url = 'http://github.com/spack/spack'
    with spack.config.override('config:use_curl', True):
        fetcher = fs.URLFetchStrategy(url=url)
        assert fetcher is not None
        with pytest.raises(TypeError, match='object is not callable'):
            with Stage(fetcher, path=testpath) as stage:
                out = stage.fetch()
            assert err_fmt.format('curl') in out
