# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.build_systems.cmake as cmake
import spack.directives
import spack.error
import spack.fetch_strategy
import spack.package_base
import spack.repo
from spack.paths import mock_packages_path
from spack.spec import Spec
from spack.util.naming import mod_to_class
from spack.version import VersionChecksumError


def pkg_factory(name):
    """Return a package object tied to an abstract spec"""
    pkg_cls = spack.repo.PATH.get_pkg_class(name)
    return pkg_cls(Spec(name))


@pytest.mark.usefixtures("config", "mock_packages")
class TestPackage:
    def test_load_package(self):
        spack.repo.PATH.get_pkg_class("mpich")

    def test_package_name(self):
        pkg_cls = spack.repo.PATH.get_pkg_class("mpich")
        assert pkg_cls.name == "mpich"

    def test_package_filename(self):
        repo = spack.repo.from_path(mock_packages_path)
        filename = repo.filename_for_package_name("mpich")
        assert filename == os.path.join(mock_packages_path, "packages", "mpich", "package.py")

    def test_nonexisting_package_filename(self):
        repo = spack.repo.from_path(mock_packages_path)
        filename = repo.filename_for_package_name("some-nonexisting-package")
        assert filename == os.path.join(
            mock_packages_path, "packages", "some-nonexisting-package", "package.py"
        )

    def test_package_class_names(self):
        assert "Mpich" == mod_to_class("mpich")
        assert "PmgrCollective" == mod_to_class("pmgr_collective")
        assert "PmgrCollective" == mod_to_class("pmgr-collective")
        assert "Pmgrcollective" == mod_to_class("PmgrCollective")
        assert "_3db" == mod_to_class("3db")

    # Below tests target direct imports of spack packages from the
    # spack.pkg namespace
    def test_import_package(self):
        import spack.pkg.builtin.mock.mpich  # type: ignore[import] # noqa: F401

    def test_import_package_as(self):
        import spack.pkg.builtin.mock  # noqa: F401
        import spack.pkg.builtin.mock as m  # noqa: F401
        import spack.pkg.builtin.mock.mpich as mp  # noqa: F401
        from spack.pkg.builtin import mock  # noqa: F401

    def test_inheritance_of_directives(self):
        pkg_cls = spack.repo.PATH.get_pkg_class("simple-inheritance")

        # Check dictionaries that should have been filled by directives
        dependencies = pkg_cls.dependencies_by_name()
        assert len(dependencies) == 3
        assert "cmake" in dependencies
        assert "openblas" in dependencies
        assert "mpi" in dependencies
        assert len(pkg_cls.provided) == 2

        # Check that Spec instantiation behaves as we expect
        s = Spec("simple-inheritance").concretized()
        assert "^cmake" in s
        assert "^openblas" in s
        assert "+openblas" in s
        assert "mpi" in s

        s = Spec("simple-inheritance~openblas").concretized()
        assert "^cmake" in s
        assert "^openblas" not in s
        assert "~openblas" in s
        assert "mpi" in s

    @pytest.mark.regression("11844")
    def test_inheritance_of_patches(self):
        s = Spec("patch-inheritance")
        # Will error if inheritor package cannot find inherited patch files
        s.concretize()

    def test_import_class_from_package(self):
        from spack.pkg.builtin.mock.mpich import Mpich  # noqa: F401

    def test_import_module_from_package(self):
        from spack.pkg.builtin.mock import mpich  # noqa: F401

    def test_import_namespace_container_modules(self):
        import spack.pkg  # noqa: F401
        import spack.pkg as p  # noqa: F401
        import spack.pkg.builtin  # noqa: F401
        import spack.pkg.builtin as b  # noqa: F401
        import spack.pkg.builtin.mock  # noqa: F401
        import spack.pkg.builtin.mock as m  # noqa: F401
        from spack import pkg  # noqa: F401
        from spack.pkg import builtin  # noqa: F401
        from spack.pkg.builtin import mock  # noqa: F401


@pytest.mark.regression("2737")
def test_urls_for_versions(mock_packages, config):
    """Version directive without a 'url' argument should use default url."""
    for spec_str in ("url_override@0.9.0", "url_override@1.0.0"):
        s = Spec(spec_str).concretized()
        url = s.package.url_for_version("0.9.0")
        assert url == "http://www.anothersite.org/uo-0.9.0.tgz"

        url = s.package.url_for_version("1.0.0")
        assert url == "http://www.doesnotexist.org/url_override-1.0.0.tar.gz"

        url = s.package.url_for_version("0.8.1")
        assert url == "http://www.doesnotexist.org/url_override-0.8.1.tar.gz"


def test_url_for_version_with_no_urls(mock_packages, config):
    spec = Spec("git-test")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    with pytest.raises(spack.error.NoURLError):
        pkg_cls(spec).url_for_version("1.0")

    with pytest.raises(spack.error.NoURLError):
        pkg_cls(spec).url_for_version("1.1")


def test_custom_cmake_prefix_path(mock_packages, config):
    spec = Spec("depends-on-define-cmake-prefix-paths").concretized()

    assert cmake.get_cmake_prefix_path(spec.package) == [
        spec["define-cmake-prefix-paths"].prefix.test
    ]


def test_url_for_version_with_only_overrides(mock_packages, config):
    s = Spec("url-only-override").concretized()

    # these exist and should just take the URL provided in the package
    assert s.package.url_for_version("1.0.0") == "http://a.example.com/url_override-1.0.0.tar.gz"
    assert s.package.url_for_version("0.9.0") == "http://b.example.com/url_override-0.9.0.tar.gz"
    assert s.package.url_for_version("0.8.1") == "http://c.example.com/url_override-0.8.1.tar.gz"

    # these don't exist but should still work, even if there are only overrides
    assert s.package.url_for_version("1.0.5") == "http://a.example.com/url_override-1.0.5.tar.gz"
    assert s.package.url_for_version("0.9.5") == "http://b.example.com/url_override-0.9.5.tar.gz"
    assert s.package.url_for_version("0.8.5") == "http://c.example.com/url_override-0.8.5.tar.gz"
    assert s.package.url_for_version("0.7.0") == "http://c.example.com/url_override-0.7.0.tar.gz"


def test_url_for_version_with_only_overrides_with_gaps(mock_packages, config):
    s = Spec("url-only-override-with-gaps").concretized()

    # same as for url-only-override -- these are specific
    assert s.package.url_for_version("1.0.0") == "http://a.example.com/url_override-1.0.0.tar.gz"
    assert s.package.url_for_version("0.9.0") == "http://b.example.com/url_override-0.9.0.tar.gz"
    assert s.package.url_for_version("0.8.1") == "http://c.example.com/url_override-0.8.1.tar.gz"

    # these don't have specific URLs, but should still work by extrapolation
    assert s.package.url_for_version("1.0.5") == "http://a.example.com/url_override-1.0.5.tar.gz"
    assert s.package.url_for_version("0.9.5") == "http://b.example.com/url_override-0.9.5.tar.gz"
    assert s.package.url_for_version("0.8.5") == "http://c.example.com/url_override-0.8.5.tar.gz"
    assert s.package.url_for_version("0.7.0") == "http://c.example.com/url_override-0.7.0.tar.gz"


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "spec_str,expected_type,expected_url",
    [
        (
            "git-top-level",
            spack.fetch_strategy.GitFetchStrategy,
            "https://example.com/some/git/repo",
        ),
        (
            "svn-top-level",
            spack.fetch_strategy.SvnFetchStrategy,
            "https://example.com/some/svn/repo",
        ),
        ("hg-top-level", spack.fetch_strategy.HgFetchStrategy, "https://example.com/some/hg/repo"),
    ],
)
def test_fetcher_url(spec_str, expected_type, expected_url):
    """Ensure that top-level git attribute can be used as a default."""
    fetcher = spack.fetch_strategy.for_package_version(pkg_factory(spec_str), "1.0")
    assert isinstance(fetcher, expected_type)
    assert fetcher.url == expected_url


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "spec_str,version_str,exception_type",
    [
        # Non-url-package
        ("git-top-level", "1.1", spack.fetch_strategy.ExtrapolationError),
        # Two VCS specified together
        ("git-url-svn-top-level", "1.0", spack.fetch_strategy.FetcherConflict),
        ("git-svn-top-level", "1.0", spack.fetch_strategy.FetcherConflict),
    ],
)
def test_fetcher_errors(spec_str, version_str, exception_type):
    """Verify that we can't extrapolate versions for non-URL packages."""
    with pytest.raises(exception_type):
        spack.fetch_strategy.for_package_version(pkg_factory(spec_str), version_str)


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "version_str,expected_url,digest",
    [
        ("2.0", "https://example.com/some/tarball-2.0.tar.gz", "20"),
        ("2.1", "https://example.com/some/tarball-2.1.tar.gz", "21"),
        ("2.2", "https://www.example.com/foo2.2.tar.gz", "22"),
        ("2.3", "https://www.example.com/foo2.3.tar.gz", "23"),
    ],
)
def test_git_url_top_level_url_versions(version_str, expected_url, digest):
    """Test URL fetch strategy inference when url is specified with git."""
    # leading 62 zeros of sha256 hash
    leading_zeros = "0" * 62

    fetcher = spack.fetch_strategy.for_package_version(
        pkg_factory("git-url-top-level"), version_str
    )
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.url == expected_url
    assert fetcher.digest == leading_zeros + digest


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "version_str,tag,commit,branch",
    [
        ("3.0", "v3.0", None, None),
        ("3.1", "v3.1", "abc31", None),
        ("3.2", None, None, "releases/v3.2"),
        ("3.3", None, "abc33", "releases/v3.3"),
        ("3.4", None, "abc34", None),
        ("submodules", None, None, None),
        ("develop", None, None, "develop"),
    ],
)
def test_git_url_top_level_git_versions(version_str, tag, commit, branch):
    """Test git fetch strategy inference when url is specified with git."""
    fetcher = spack.fetch_strategy.for_package_version(
        pkg_factory("git-url-top-level"), version_str
    )
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == "https://example.com/some/git/repo"
    assert fetcher.tag == tag
    assert fetcher.commit == commit
    assert fetcher.branch == branch
    assert fetcher.url == pkg_factory("git-url-top-level").git


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize("version_str", ["1.0", "1.1", "1.2", "1.3"])
def test_git_url_top_level_conflicts(version_str):
    """Test git fetch strategy inference when url is specified with git."""
    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg_factory("git-url-top-level"), version_str)


def test_rpath_args(mutable_database):
    """Test a package's rpath_args property."""

    rec = mutable_database.get_record("mpich")

    rpath_args = rec.spec.package.rpath_args
    assert "-rpath" in rpath_args
    assert "mpich" in rpath_args


def test_bundle_version_checksum(mock_directive_bundle, clear_directive_functions):
    """Test raising exception on a version checksum with a bundle package."""
    with pytest.raises(VersionChecksumError, match="Checksums not allowed"):
        version = spack.directives.version("1.0", checksum="1badpkg")
        version(mock_directive_bundle)


def test_bundle_patch_directive(mock_directive_bundle, clear_directive_functions):
    """Test raising exception on a patch directive with a bundle package."""
    with pytest.raises(
        spack.directives.UnsupportedPackageDirective, match="Patches are not allowed"
    ):
        patch = spack.directives.patch("mock/patch.txt")
        patch(mock_directive_bundle)


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "version_str,digest_end,extra_options",
    [
        ("1.0", "10", {"timeout": 42, "cookie": "foobar"}),
        ("1.1", "11", {"timeout": 65}),
        ("1.2", "12", {"cookie": "baz"}),
    ],
)
def test_fetch_options(version_str, digest_end, extra_options):
    """Test fetch options inference."""
    leading_zeros = "000000000000000000000000000000"
    fetcher = spack.fetch_strategy.for_package_version(pkg_factory("fetch-options"), version_str)
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.digest == leading_zeros + digest_end
    assert fetcher.extra_options == extra_options


def test_package_deprecated_version(mock_packages, mock_fetch, mock_stage):
    spec = Spec("deprecated-versions")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)

    assert spack.package_base.deprecated_version(pkg_cls, "1.1.0")
    assert not spack.package_base.deprecated_version(pkg_cls, "1.0.0")


def test_package_can_have_sparse_checkout_properties(mock_packages, mock_fetch, mock_stage):
    spec = Spec("git-sparsepaths-pkg")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    assert hasattr(pkg_cls, "git_sparse_paths")

    fetcher = spack.fetch_strategy.for_package_version(pkg_cls(spec), "1.0")
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert hasattr(fetcher, "git_sparse_paths")
    assert fetcher.git_sparse_paths == pkg_cls.git_sparse_paths
