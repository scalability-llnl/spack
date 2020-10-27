# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import pytest

import spack.repo
import spack.mirror
import spack.util.executable
import spack.util.url
import spack.util.web
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which

from llnl.util.filesystem import resolve_link_target_relative_to_the_link

pytestmark = pytest.mark.usefixtures('config', 'mutable_mock_repo')

# paths in repos that shouldn't be in the mirror tarballs.
exclude = ['.hg', '.git', '.svn']


repos = {}


def set_up_package(name, repository, url_attr):
    """Set up a mock package to be mirrored.
    Each package needs us to:

    1. Set up a mock repo/archive to fetch from.
    2. Point the package's version args at that repo.
    """
    # Set up packages to point at mock repos.
    spec = Spec(name)
    spec.concretize()
    # Get the package and fix its fetch args to point to a mock repo
    pkg = spack.repo.get(spec)

    repos[name] = repository

    # change the fetch args of the first (only) version.
    assert len(pkg.versions) == 1
    v = next(iter(pkg.versions))

    pkg.versions[v][url_attr] = repository.url


def check_mirror():
    with Stage('spack-mirror-test') as stage:
        mirror_root = os.path.join(stage.path, 'test-mirror')
        # register mirror with spack config
        mirrors = {'spack-mirror-test': 'file://' + mirror_root}
        with spack.config.override('mirrors', mirrors):
            with spack.config.override('config:checksum', False):
                specs = [Spec(x).concretized() for x in repos]
                spack.mirror.create(mirror_root, specs)

            # Stage directory exists
            assert os.path.isdir(mirror_root)

            for spec in specs:
                fetcher = spec.package.fetcher[0]
                per_package_ref = os.path.join(
                    spec.name, '-'.join([spec.name, str(spec.version)]))
                mirror_paths = spack.mirror.mirror_archive_paths(
                    fetcher,
                    per_package_ref)
                expected_path = os.path.join(
                    mirror_root, mirror_paths.storage_path)
                assert os.path.exists(expected_path)

            # Now try to fetch each package.
            for name, mock_repo in repos.items():
                spec = Spec(name).concretized()
                pkg = spec.package

                with spack.config.override('config:checksum', False):
                    with pkg.stage:
                        pkg.do_stage(mirror_only=True)

                        # Compare the original repo with the expanded archive
                        original_path = mock_repo.path
                        if 'svn' in name:
                            # have to check out the svn repo to compare.
                            original_path = os.path.join(
                                mock_repo.path, 'checked_out')

                            svn = which('svn', required=True)
                            svn('checkout', mock_repo.url, original_path)

                        dcmp = filecmp.dircmp(
                            original_path, pkg.stage.source_path)

                        # make sure there are no new files in the expanded
                        # tarball
                        assert not dcmp.right_only
                        # and that all original files are present.
                        assert all(
                            original_file in exclude
                            for original_file in dcmp.left_only)


def test_url_mirror(mock_archive):
    set_up_package('trivial-install-test-package', mock_archive, 'url')
    check_mirror()
    repos.clear()


def test_bad_mirror_args():
    mirror_from_args = (
        lambda directory=None, mirror_name=None, mirror_url=None:
            spack.mirror.Mirror.from_args(type('', (), {
                'directory': directory,
                'mirror_name': mirror_name,
                'mirror_url': mirror_url
            })))

    # Must provide no more than one of either directory, mirror_name, or
    # mirror_url arguments
    with pytest.raises(ValueError):
        mirror_from_args(
            directory='some-directory',
            mirror_name='some-mirror-name',
            mirror_url='some-mirror-url')

    with pytest.raises(ValueError):
        mirror_from_args(
            directory='some-directory',
            mirror_name='some-mirror-name')

    with pytest.raises(ValueError):
        mirror_from_args(
            directory='some-directory',
            mirror_url='some-mirror-url')

    with pytest.raises(ValueError):
        mirror_from_args(
            mirror_name='some-mirror-name',
            mirror_url='some-mirror-url')

    # No arguments: return default mirror, which should be source_cache
    cache = spack.config.get('config:source_cache')
    default_mirror = mirror_from_args()

    assert default_mirror.fetch_url == cache
    assert default_mirror.push_url == cache

    # BAD: callsite passes something other than a directory via "directory"
    with pytest.raises(ValueError):
        mirror_from_args(directory='https://spack.io/example')

    # BAD: callsite passes a mirror_name that doesn't map to a pre-configured
    #      mirror.
    with pytest.raises(ValueError):
        mirror_from_args(mirror_name='-[@&%-not-a-valid-"-mirror-name-%&@]-')

    # BAD: callsite passes a mirror_url that is not a URL
    with pytest.raises(ValueError):
        mirror_from_args(mirror_url='/user/forgot/to/prepend/file://')


@pytest.mark.skipif(
    not which('git'), reason='requires git to be installed')
def test_git_mirror(mock_git_repository):
    set_up_package('git-test', mock_git_repository, 'git')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not which('svn') or not which('svnadmin'),
    reason='requires subversion to be installed')
def test_svn_mirror(mock_svn_repository):
    set_up_package('svn-test', mock_svn_repository, 'svn')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not which('hg'), reason='requires mercurial to be installed')
def test_hg_mirror(mock_hg_repository):
    set_up_package('hg-test', mock_hg_repository, 'hg')
    check_mirror()
    repos.clear()


@pytest.mark.skipif(
    not all([which('svn'), which('hg'), which('git')]),
    reason='requires subversion, git, and mercurial to be installed')
def test_all_mirror(
        mock_git_repository,
        mock_svn_repository,
        mock_hg_repository,
        mock_archive):

    set_up_package('git-test', mock_git_repository, 'git')
    set_up_package('svn-test', mock_svn_repository, 'svn')
    set_up_package('hg-test', mock_hg_repository, 'hg')
    set_up_package('trivial-install-test-package', mock_archive, 'url')
    check_mirror()
    repos.clear()


def test_mirror_archive_paths_no_version(mock_packages, config, mock_archive):
    spec = Spec('trivial-install-test-package@nonexistingversion')
    fetcher = spack.fetch_strategy.URLFetchStrategy(mock_archive.url)
    spack.mirror.mirror_archive_paths(fetcher, 'per-package-ref', spec)


def test_mirror_with_url_patches(mock_packages, config, monkeypatch):
    spec = Spec('patch-several-dependencies')
    spec.concretize()

    files_cached_in_mirror = set()

    def record_store(_class, fetcher, relative_dst, cosmetic_path=None):
        files_cached_in_mirror.add(os.path.basename(relative_dst))

    def successful_fetch(_class):
        with open(_class.stage.save_filename, 'w'):
            pass

    def successful_expand(_class):
        expanded_path = os.path.join(_class.stage.path,
                                     spack.stage._source_path_subdir)
        os.mkdir(expanded_path)
        with open(os.path.join(expanded_path, 'test.patch'), 'w'):
            pass

    def successful_apply(*args, **kwargs):
        pass

    with Stage('spack-mirror-test') as stage:
        mirror_root = os.path.join(stage.path, 'test-mirror')

        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, 'fetch',
                            successful_fetch)
        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy,
                            'expand', successful_expand)
        monkeypatch.setattr(spack.patch, 'apply_patch', successful_apply)
        monkeypatch.setattr(spack.caches.MirrorCache, 'store', record_store)

        with spack.config.override('config:checksum', False):
            spack.mirror.create(mirror_root, list(spec.traverse()))

        assert not (set([
            'abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234',
            'abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd.gz'  # NOQA: ignore=E501
        ]) - files_cached_in_mirror)


class MockFetcher(object):
    """Mock fetcher object which implements the necessary functionality for
       testing MirrorCache
    """
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir

    def archive(self, dst):
        filename = os.path.join(self.tmpdir, 'empty-file')
        with open(filename, 'w'):
            pass
        spack.util.web.push_to_url(filename, dst, keep_original=False)


@pytest.mark.regression('14067')
def test_mirror_cache_symlinks(tmpdir):
    """Confirm that the cosmetic symlink created in the mirror cache (which may
       be relative) targets the storage path correctly.
    """
    cosmetic_path = 'zlib/zlib-1.2.11.tar.gz'
    global_path = '_source-cache/archive/c3/c3e5.tar.gz'
    cache = spack.caches.MirrorCache(str(tmpdir), False)
    reference = spack.mirror.MirrorReference(cosmetic_path, global_path)

    cache.store(MockFetcher(tmpdir), reference.storage_path)
    cache.symlink(reference)

    cache_root = spack.util.url.local_file_path(cache.root)
    link_target = resolve_link_target_relative_to_the_link(
        os.path.join(cache_root, reference.cosmetic_path))
    assert os.path.exists(link_target)
    assert (os.path.normpath(link_target) ==
            os.path.join(cache_root, reference.storage_path))
