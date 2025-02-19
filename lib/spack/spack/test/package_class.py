# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test class methods on Package objects.

This doesn't include methods on package *instances* (like do_patch(),
etc.).  Only methods like ``possible_dependencies()`` that deal with the
static DSL metadata for packages.
"""

import os
import shutil

import pytest

import llnl.util.filesystem as fs

import spack.binary_distribution
import spack.compilers
import spack.concretize
import spack.deptypes as dt
import spack.error
import spack.install_test
import spack.package
import spack.package_base
import spack.spec
import spack.store
from spack.build_systems.generic import Package
from spack.error import InstallError
from spack.solver.input_analysis import NoStaticAnalysis, StaticAnalysis


@pytest.fixture()
def mpileaks_possible_deps(mock_packages, mpi_names):
    possible = {
        "callpath": set(["dyninst"] + mpi_names),
        "low-priority-provider": set(),
        "dyninst": set(["libdwarf", "libelf"]),
        "fake": set(),
        "intel-parallel-studio": set(),
        "libdwarf": set(["libelf"]),
        "libelf": set(),
        "mpich": set(),
        "mpich2": set(),
        "mpileaks": set(["callpath"] + mpi_names),
        "multi-provider-mpi": set(),
        "zmpi": set(["fake"]),
    }
    return possible


@pytest.fixture(params=[NoStaticAnalysis, StaticAnalysis])
def mock_inspector(config, mock_packages, request):
    inspector_cls = request.param
    if inspector_cls is NoStaticAnalysis:
        return inspector_cls(configuration=config, repo=mock_packages)
    return inspector_cls(
        configuration=config,
        repo=mock_packages,
        store=spack.store.STORE,
        binary_index=spack.binary_distribution.BINARY_INDEX,
    )


@pytest.fixture
def mpi_names(mock_inspector):
    return [spec.name for spec in mock_inspector.providers_for("mpi")]


@pytest.mark.parametrize(
    "pkg_name,fn_kwargs,expected",
    [
        (
            "mpileaks",
            {"expand_virtuals": True, "allowed_deps": dt.ALL},
            {
                "fake",
                "mpileaks",
                "multi-provider-mpi",
                "callpath",
                "dyninst",
                "mpich2",
                "libdwarf",
                "zmpi",
                "low-priority-provider",
                "intel-parallel-studio",
                "mpich",
                "libelf",
            },
        ),
        (
            "mpileaks",
            {"expand_virtuals": False, "allowed_deps": dt.ALL},
            {"callpath", "dyninst", "libdwarf", "libelf", "mpileaks"},
        ),
        (
            "mpileaks",
            {"expand_virtuals": False, "allowed_deps": dt.ALL, "transitive": False},
            {"callpath", "mpileaks"},
        ),
        ("dtbuild1", {"allowed_deps": dt.LINK | dt.RUN}, {"dtbuild1", "dtrun2", "dtlink2"}),
        ("dtbuild1", {"allowed_deps": dt.BUILD}, {"dtbuild1", "dtbuild2", "dtlink2"}),
        ("dtbuild1", {"allowed_deps": dt.LINK}, {"dtbuild1", "dtlink2"}),
    ],
)
def test_possible_dependencies(pkg_name, fn_kwargs, expected, mock_runtimes, mock_inspector):
    """Tests possible nodes of mpileaks, under different scenarios."""
    expected.update(mock_runtimes)
    result, *_ = mock_inspector.possible_dependencies(pkg_name, **fn_kwargs)
    assert expected == result


def test_possible_dependencies_virtual(mock_inspector, mock_packages, mock_runtimes, mpi_names):
    expected = set(mpi_names)
    for name in mpi_names:
        expected.update(dep for dep in mock_packages.get_pkg_class(name).dependencies_by_name())
    expected.update(mock_runtimes)

    real_pkgs, *_ = mock_inspector.possible_dependencies(
        "mpi", transitive=False, allowed_deps=dt.ALL
    )
    assert expected == real_pkgs


def test_possible_dependencies_missing(mock_inspector):
    result, *_ = mock_inspector.possible_dependencies("missing-dependency", allowed_deps=dt.ALL)
    assert "this-is-a-missing-dependency" not in result


def test_possible_dependencies_with_multiple_classes(
    mock_inspector, mock_packages, mpileaks_possible_deps
):
    pkgs = ["dt-diamond", "mpileaks"]
    expected = set(mpileaks_possible_deps)
    expected.update({"dt-diamond", "dt-diamond-left", "dt-diamond-right", "dt-diamond-bottom"})
    expected.update(mock_packages.packages_with_tags("runtime"))

    real_pkgs, *_ = mock_inspector.possible_dependencies(*pkgs, allowed_deps=dt.ALL)
    assert set(expected) == real_pkgs


def setup_install_test(source_paths, test_root):
    """
    Set up the install test by creating sources and install test roots.

    The convention used here is to create an empty file if the path name
    ends with an extension otherwise, a directory is created.
    """
    fs.mkdirp(test_root)
    for path in source_paths:
        if os.path.splitext(path)[1]:
            fs.touchp(path)
        else:
            fs.mkdirp(path)


@pytest.mark.parametrize(
    "spec,sources,extras,expect",
    [
        (
            "pkg-a",
            ["example/a.c"],  # Source(s)
            ["example/a.c"],  # Extra test source
            ["example/a.c"],
        ),  # Test install dir source(s)
        (
            "pkg-b",
            ["test/b.cpp", "test/b.hpp", "example/b.txt"],  # Source(s)
            ["test"],  # Extra test source
            ["test/b.cpp", "test/b.hpp"],
        ),  # Test install dir source
        (
            "pkg-c",
            ["examples/a.py", "examples/b.py", "examples/c.py", "tests/d.py"],
            ["examples/b.py", "tests"],
            ["examples/b.py", "tests/d.py"],
        ),
    ],
)
def test_cache_extra_sources(install_mockery, spec, sources, extras, expect):
    """Test the package's cache extra test sources helper function."""
    s = spack.concretize.concretize_one(spec)

    source_path = s.package.stage.source_path
    srcs = [fs.join_path(source_path, src) for src in sources]
    test_root = spack.install_test.install_test_root(s.package)
    setup_install_test(srcs, test_root)

    emsg_dir = "Expected {0} to be a directory"
    emsg_file = "Expected {0} to be a file"
    for src in srcs:
        assert os.path.exists(src), "Expected {0} to exist".format(src)
        if os.path.splitext(src)[1]:
            assert os.path.isfile(src), emsg_file.format(src)
        else:
            assert os.path.isdir(src), emsg_dir.format(src)

    spack.install_test.cache_extra_test_sources(s.package, extras)

    src_dests = [fs.join_path(test_root, src) for src in sources]
    exp_dests = [fs.join_path(test_root, e) for e in expect]
    poss_dests = set(src_dests) | set(exp_dests)

    msg = "Expected {0} to{1} exist"
    for pd in poss_dests:
        if pd in exp_dests:
            assert os.path.exists(pd), msg.format(pd, "")
            if os.path.splitext(pd)[1]:
                assert os.path.isfile(pd), emsg_file.format(pd)
            else:
                assert os.path.isdir(pd), emsg_dir.format(pd)
        else:
            assert not os.path.exists(pd), msg.format(pd, " not")

    # Perform a little cleanup
    shutil.rmtree(os.path.dirname(source_path))


def test_cache_extra_sources_fails(install_mockery):
    s = spack.concretize.concretize_one("pkg-a")

    with pytest.raises(InstallError) as exc_info:
        spack.install_test.cache_extra_test_sources(s.package, ["/a/b", "no-such-file"])

    errors = str(exc_info.value)
    assert "'/a/b') must be relative" in errors
    assert "'no-such-file') for the copy does not exist" in errors


def test_package_exes_and_libs():
    with pytest.raises(spack.error.SpackError, match="defines both"):

        class BadDetectablePackage(spack.package.Package):
            executables = ["findme"]
            libraries = ["libFindMe.a"]


def test_package_url_and_urls():
    class URLsPackage(spack.package.Package):
        url = "https://www.example.com/url-package-1.0.tgz"
        urls = ["https://www.example.com/archive"]

    s = spack.spec.Spec("pkg-a")
    with pytest.raises(ValueError, match="defines both"):
        URLsPackage(s)


def test_package_license():
    class LicensedPackage(spack.package.Package):
        extendees = None  # currently a required attribute for is_extension()
        license_files = None

    s = spack.spec.Spec("pkg-a")
    pkg = LicensedPackage(s)
    assert pkg.global_license_file is None

    pkg.license_files = ["license.txt"]
    assert os.path.basename(pkg.global_license_file) == pkg.license_files[0]


class BaseTestPackage(Package):
    extendees = None  # currently a required attribute for is_extension()


def test_package_version_fails():
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    with pytest.raises(ValueError, match="does not have a concrete version"):
        pkg.version()


def test_package_tester_fails():
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    with pytest.raises(ValueError, match="without concrete version"):
        pkg.tester()


def test_package_fetcher_fails():
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    with pytest.raises(ValueError, match="without concrete version"):
        pkg.fetcher


def test_package_test_no_compilers(mock_packages, monkeypatch, capfd):
    def compilers(compiler, arch_spec):
        return None

    monkeypatch.setattr(spack.compilers, "compilers_for_spec", compilers)

    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    pkg.test_requires_compiler = True
    pkg.do_test()
    error = capfd.readouterr()[1]
    assert "Skipping tests for package" in error
    assert "test requires missing compiler" in error


def test_package_subscript(default_mock_concretization):
    """Tests that we can use the subscript notation on packages, and that it returns a package"""
    root = default_mock_concretization("mpileaks")
    root_pkg = root.package

    # Subscript of a virtual
    assert isinstance(root_pkg["mpi"], spack.package_base.PackageBase)

    # Subscript on concrete
    for d in root.traverse():
        assert isinstance(root_pkg[d.name], spack.package_base.PackageBase)
