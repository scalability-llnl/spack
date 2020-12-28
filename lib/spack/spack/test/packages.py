# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import pytest

import spack.repo
import spack.fetch_strategy
from spack.paths import mock_packages_path
from spack.util.naming import mod_to_class
from spack.spec import Spec
from spack.util.package_hash import package_content
from spack.version import VersionChecksumError
import spack.directives


def _generate_content_strip_name(spec):
    content = package_content(spec)
    return content.replace(spec.package.__class__.__name__, '')


@pytest.mark.usefixtures('config', 'mock_packages')
class TestPackage(object):
    def test_load_package(self):
        spack.repo.get('mpich')

    def test_package_name(self):
        pkg = spack.repo.get('mpich')
        assert pkg.name == 'mpich'

    def test_package_filename(self):
        repo = spack.repo.Repo(mock_packages_path)
        filename = repo.filename_for_package_name('mpich')
        assert filename == os.path.join(
            mock_packages_path,
            'packages',
            'mpich',
            'package.py'
        )

    def test_nonexisting_package_filename(self):
        repo = spack.repo.Repo(mock_packages_path)
        filename = repo.filename_for_package_name('some-nonexisting-package')
        assert filename == os.path.join(
            mock_packages_path,
            'packages',
            'some-nonexisting-package',
            'package.py'
        )

    def test_package_class_names(self):
        assert 'Mpich' == mod_to_class('mpich')
        assert 'PmgrCollective' == mod_to_class('pmgr_collective')
        assert 'PmgrCollective' == mod_to_class('pmgr-collective')
        assert 'Pmgrcollective' == mod_to_class('PmgrCollective')
        assert '_3db' == mod_to_class('3db')

    def test_content_hash_all_same_but_patch_contents(self):
        spec1 = Spec("hash-test1@1.1").concretized()
        spec2 = Spec("hash-test2@1.1").concretized()
        content1 = _generate_content_strip_name(spec1)
        content2 = _generate_content_strip_name(spec2)
        assert spec1.package.content_hash(content=content1) != \
            spec2.package.content_hash(content=content2)

    def test_content_hash_different_variants(self):
        spec1 = Spec("hash-test1@1.2 +variantx").concretized()
        spec2 = Spec("hash-test2@1.2 ~variantx").concretized()
        content1 = _generate_content_strip_name(spec1)
        content2 = _generate_content_strip_name(spec2)
        assert spec1.package.content_hash(content=content1) == \
            spec2.package.content_hash(content=content2)

    def test_content_hash_cannot_get_details_from_ast(self):
        """Packages hash-test1 and hash-test3 would be considered the same
           except that hash-test3 conditionally executes a phase based on
           a "when" directive that Spack cannot evaluate by examining the
           AST. This test ensures that Spack can compute a content hash
           for hash-test3. If Spack cannot determine when a phase applies,
           it adds it by default, so the test also ensures that the hashes
           differ where Spack includes a phase on account of AST-examination
           failure.
        """
        spec3 = Spec("hash-test1@1.7").concretized()
        spec4 = Spec("hash-test3@1.7").concretized()
        content3 = _generate_content_strip_name(spec3)
        content4 = _generate_content_strip_name(spec4)
        assert(spec3.package.content_hash(content=content3) !=
               spec4.package.content_hash(content=content4))

    def test_all_same_but_archive_hash(self):
        spec1 = Spec("hash-test1@1.3").concretized()
        spec2 = Spec("hash-test2@1.3").concretized()
        content1 = _generate_content_strip_name(spec1)
        content2 = _generate_content_strip_name(spec2)
        assert spec1.package.content_hash(content=content1) != \
            spec2.package.content_hash(content=content2)

    def test_parse_dynamic_function_call(self):
        spec = Spec("hash-test4").concretized()
        spec.package.content_hash()

    # Below tests target direct imports of spack packages from the
    # spack.pkg namespace
    def test_import_package(self):
        import spack.pkg.builtin.mock.mpich             # noqa

    def test_import_package_as(self):
        import spack.pkg.builtin.mock.mpich as mp       # noqa

        import spack.pkg.builtin.mock                   # noqa
        import spack.pkg.builtin.mock as m              # noqa
        from spack.pkg.builtin import mock              # noqa

    def test_inheritance_of_diretives(self):
        p = spack.repo.get('simple-inheritance')

        # Check dictionaries that should have been filled by directives
        assert len(p.dependencies) == 3
        assert 'cmake' in p.dependencies
        assert 'openblas' in p.dependencies
        assert 'mpi' in p.dependencies
        assert len(p.provided) == 2

        # Check that Spec instantiation behaves as we expect
        s = Spec('simple-inheritance')
        s.concretize()
        assert '^cmake' in s
        assert '^openblas' in s
        assert '+openblas' in s
        assert 'mpi' in s

        s = Spec('simple-inheritance~openblas')
        s.concretize()
        assert '^cmake' in s
        assert '^openblas' not in s
        assert '~openblas' in s
        assert 'mpi' in s

    @pytest.mark.regression('11844')
    def test_inheritance_of_patches(self):
        s = Spec('patch-inheritance')
        # Will error if inheritor package cannot find inherited patch files
        s.concretize()

    def test_dependency_extensions(self):
        s = Spec('extension2')
        s.concretize()
        deps = set(x.name for x in s.package.dependency_activations())
        assert deps == set(['extension1'])

    def test_import_class_from_package(self):
        from spack.pkg.builtin.mock.mpich import Mpich  # noqa

    def test_import_module_from_package(self):
        from spack.pkg.builtin.mock import mpich        # noqa

    def test_import_namespace_container_modules(self):
        import spack.pkg                                # noqa
        import spack.pkg as p                           # noqa
        from spack import pkg                           # noqa

        import spack.pkg.builtin                        # noqa
        import spack.pkg.builtin as b                   # noqa
        from spack.pkg import builtin                   # noqa

        import spack.pkg.builtin.mock                   # noqa
        import spack.pkg.builtin.mock as m              # noqa
        from spack.pkg.builtin import mock              # noqa


@pytest.mark.regression('2737')
def test_urls_for_versions(mock_packages, config):
    """Version directive without a 'url' argument should use default url."""
    for spec_str in ('url_override@0.9.0', 'url_override@1.0.0'):
        s = Spec(spec_str).concretized()
        url = s.package.url_for_version('0.9.0')
        assert url == 'http://www.anothersite.org/uo-0.9.0.tgz'

        url = s.package.url_for_version('1.0.0')
        assert url == 'http://www.doesnotexist.org/url_override-1.0.0.tar.gz'

        url = s.package.url_for_version('0.8.1')
        assert url == 'http://www.doesnotexist.org/url_override-0.8.1.tar.gz'


def test_url_for_version_with_no_urls(mock_packages, config):
    pkg = spack.repo.get('git-test')
    with pytest.raises(spack.package_base.NoURLError):
        pkg.url_for_version('1.0')

    with pytest.raises(spack.package_base.NoURLError):
        pkg.url_for_version('1.1')


def test_url_for_version_with_only_overrides(mock_packages, config):
    spec = Spec('url-only-override')
    spec.concretize()

    pkg = spack.repo.get(spec)

    # these exist and should just take the URL provided in the package
    assert pkg.url_for_version('1.0.0') == 'http://a.example.com/url_override-1.0.0.tar.gz'
    assert pkg.url_for_version('0.9.0') == 'http://b.example.com/url_override-0.9.0.tar.gz'
    assert pkg.url_for_version('0.8.1') == 'http://c.example.com/url_override-0.8.1.tar.gz'

    # these don't exist but should still work, even if there are only overrides
    assert pkg.url_for_version('1.0.5') == 'http://a.example.com/url_override-1.0.5.tar.gz'
    assert pkg.url_for_version('0.9.5') == 'http://b.example.com/url_override-0.9.5.tar.gz'
    assert pkg.url_for_version('0.8.5') == 'http://c.example.com/url_override-0.8.5.tar.gz'
    assert pkg.url_for_version('0.7.0') == 'http://c.example.com/url_override-0.7.0.tar.gz'


def test_url_for_version_with_only_overrides_with_gaps(mock_packages, config):
    spec = Spec('url-only-override-with-gaps')
    spec.concretize()

    pkg = spack.repo.get(spec)

    # same as for url-only-override -- these are specific
    assert pkg.url_for_version('1.0.0') == 'http://a.example.com/url_override-1.0.0.tar.gz'
    assert pkg.url_for_version('0.9.0') == 'http://b.example.com/url_override-0.9.0.tar.gz'
    assert pkg.url_for_version('0.8.1') == 'http://c.example.com/url_override-0.8.1.tar.gz'

    # these don't have specific URLs, but should still work by extrapolation
    assert pkg.url_for_version('1.0.5') == 'http://a.example.com/url_override-1.0.5.tar.gz'
    assert pkg.url_for_version('0.9.5') == 'http://b.example.com/url_override-0.9.5.tar.gz'
    assert pkg.url_for_version('0.8.5') == 'http://c.example.com/url_override-0.8.5.tar.gz'
    assert pkg.url_for_version('0.7.0') == 'http://c.example.com/url_override-0.7.0.tar.gz'


def test_git_top_level(mock_packages, config):
    """Ensure that top-level git attribute can be used as a default."""
    pkg = spack.repo.get('git-top-level')

    fetcher = spack.fetch_strategy.for_package_version(pkg, '1.0')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'


def test_svn_top_level(mock_packages, config):
    """Ensure that top-level svn attribute can be used as a default."""
    pkg = spack.repo.get('svn-top-level')

    fetcher = spack.fetch_strategy.for_package_version(pkg, '1.0')
    assert isinstance(fetcher, spack.fetch_strategy.SvnFetchStrategy)
    assert fetcher.url == 'https://example.com/some/svn/repo'


def test_hg_top_level(mock_packages, config):
    """Ensure that top-level hg attribute can be used as a default."""
    pkg = spack.repo.get('hg-top-level')

    fetcher = spack.fetch_strategy.for_package_version(pkg, '1.0')
    assert isinstance(fetcher, spack.fetch_strategy.HgFetchStrategy)
    assert fetcher.url == 'https://example.com/some/hg/repo'


def test_no_extrapolate_without_url(mock_packages, config):
    """Verify that we can't extrapolate versions for non-URL packages."""
    pkg = spack.repo.get('git-top-level')

    with pytest.raises(spack.fetch_strategy.ExtrapolationError):
        spack.fetch_strategy.for_package_version(pkg, '1.1')


def test_two_vcs_fetchers_top_level(mock_packages, config):
    """Verify conflict when two VCS strategies are specified together."""

    pkg = spack.repo.get('git-url-svn-top-level')
    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg, '1.0')

    pkg = spack.repo.get('git-svn-top-level')
    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg, '1.0')


def test_git_url_top_level_url_versions(mock_packages, config):
    """Test URL fetch strategy inference when url is specified with git."""

    pkg = spack.repo.get('git-url-top-level')

    fetcher = spack.fetch_strategy.for_package_version(pkg, '2.0')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.url == 'https://example.com/some/tarball-2.0.tar.gz'
    assert fetcher.digest == 'abc20'

    fetcher = spack.fetch_strategy.for_package_version(pkg, '2.1')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.url == 'https://example.com/some/tarball-2.1.tar.gz'
    assert fetcher.digest == 'abc21'

    fetcher = spack.fetch_strategy.for_package_version(pkg, '2.2')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.url == 'https://www.example.com/foo2.2.tar.gz'
    assert fetcher.digest == 'abc22'

    fetcher = spack.fetch_strategy.for_package_version(pkg, '2.3')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.url == 'https://www.example.com/foo2.3.tar.gz'
    assert fetcher.digest == 'abc23'


def test_git_url_top_level_git_versions(mock_packages, config):
    """Test git fetch strategy inference when url is specified with git."""

    pkg = spack.repo.get('git-url-top-level')

    fetcher = spack.fetch_strategy.for_package_version(pkg, '3.0')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag == 'v3.0'
    assert fetcher.commit is None
    assert fetcher.branch is None

    fetcher = spack.fetch_strategy.for_package_version(pkg, '3.1')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag == 'v3.1'
    assert fetcher.commit == 'abc31'
    assert fetcher.branch is None

    fetcher = spack.fetch_strategy.for_package_version(pkg, '3.2')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag is None
    assert fetcher.commit is None
    assert fetcher.branch == 'releases/v3.2'

    fetcher = spack.fetch_strategy.for_package_version(pkg, '3.3')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag is None
    assert fetcher.commit == 'abc33'
    assert fetcher.branch == 'releases/v3.3'

    fetcher = spack.fetch_strategy.for_package_version(pkg, '3.4')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag is None
    assert fetcher.commit == 'abc34'
    assert fetcher.branch is None

    fetcher = spack.fetch_strategy.for_package_version(pkg, 'submodules')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag is None
    assert fetcher.commit is None
    assert fetcher.branch is None

    fetcher = spack.fetch_strategy.for_package_version(pkg, 'develop')
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == 'https://example.com/some/git/repo'
    assert fetcher.tag is None
    assert fetcher.commit is None
    assert fetcher.branch == 'develop'


def test_git_url_top_level_conflicts(mock_packages, config):
    """Test git fetch strategy inference when url is specified with git."""

    pkg = spack.repo.get('git-url-top-level')

    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg, '1.0')

    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg, '1.1')

    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg, '1.2')

    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg, '1.3')


def test_rpath_args(mutable_database):
    """Test a package's rpath_args property."""

    rec = mutable_database.get_record('mpich')

    rpath_args = rec.spec.package.rpath_args
    assert '-rpath' in rpath_args
    assert 'mpich' in rpath_args


def test_bundle_version_checksum(mock_directive_bundle,
                                 clear_directive_functions):
    """Test raising exception on a version checksum with a bundle package."""
    with pytest.raises(VersionChecksumError, match="Checksums not allowed"):
        version = spack.directives.version('1.0', checksum='1badpkg')
        version(mock_directive_bundle)


def test_bundle_patch_directive(mock_directive_bundle,
                                clear_directive_functions):
    """Test raising exception on a patch directive with a bundle package."""
    with pytest.raises(spack.directives.UnsupportedPackageDirective,
                       match="Patches are not allowed"):
        patch = spack.directives.patch('mock/patch.txt')
        patch(mock_directive_bundle)


def test_fetch_options(mock_packages, config):
    """Test fetch options inference."""

    pkg = spack.repo.get('fetch-options')

    fetcher = spack.fetch_strategy.for_package_version(pkg, '1.0')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.digest == 'abc10'
    assert fetcher.extra_options == {'timeout': 42, 'cookie': 'foobar'}

    fetcher = spack.fetch_strategy.for_package_version(pkg, '1.1')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.digest == 'abc11'
    assert fetcher.extra_options == {'timeout': 65}

    fetcher = spack.fetch_strategy.for_package_version(pkg, '1.2')
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.digest == 'abc12'
    assert fetcher.extra_options == {'cookie': 'baz'}
