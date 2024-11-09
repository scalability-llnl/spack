# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import filecmp
import os
import shutil
import sys

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

import spack.error
import spack.fetch_strategy
import spack.patch
import spack.paths
import spack.repo
import spack.spec
import spack.stage
import spack.util.url as url_util
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import Executable

# various sha256 sums (using variables for legibility)
# many file based shas will differ between Windows and other platforms
# due to the use of carriage returns ('\r\n') in Windows line endings

# files with contents 'foo', 'bar', and 'baz'
foo_sha256 = (
    "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c"
    if sys.platform != "win32"
    else "bf874c7dd3a83cf370fdc17e496e341de06cd596b5c66dbf3c9bb7f6c139e3ee"
)
bar_sha256 = (
    "7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730"
    if sys.platform != "win32"
    else "556ddc69a75d0be0ecafc82cd4657666c8063f13d762282059c39ff5dbf18116"
)
baz_sha256 = (
    "bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c"
    if sys.platform != "win32"
    else "d30392e66c636a063769cbb1db08cd3455a424650d4494db6379d73ea799582b"
)
biz_sha256 = (
    "a69b288d7393261e613c276c6d38a01461028291f6e381623acc58139d01f54d"
    if sys.platform != "win32"
    else "2f2b087a8f84834fd03d4d1d5b43584011e869e4657504ef3f8b0a672a5c222e"
)

# url patches
# url shas are the same on Windows
url1_sha256 = "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
url2_sha256 = "1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd"
url2_archive_sha256 = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"

platform_url_sha = (
    "252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866"
    if sys.platform != "win32"
    else "ecf44a8244a486e9ef5f72c6cb622f99718dcd790707ac91af0b8c9a4ab7a2bb"
)


@pytest.fixture()
def mock_patch_stage(tmpdir_factory, monkeypatch):
    # Don't disrupt the spack install directory with tests.
    mock_path = str(tmpdir_factory.mktemp("mock-patch-stage"))
    monkeypatch.setattr(spack.stage, "_stage_root", mock_path)
    return mock_path


data_path = os.path.join(spack.paths.test_path, "data", "patch")


@pytest.mark.not_on_windows("Line ending conflict on Windows")
@pytest.mark.parametrize(
    "filename, sha256, archive_sha256",
    [
        # compressed patch -- needs sha256 and archive_256
        (
            os.path.join(data_path, "foo.tgz"),
            "252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866",
            "4e8092a161ec6c3a1b5253176fcf33ce7ba23ee2ff27c75dbced589dabacd06e",
        ),
        # uncompressed patch -- needs only sha256
        (os.path.join(data_path, "foo.patch"), platform_url_sha, None),
    ],
)
def test_url_patch(mock_patch_stage, filename, sha256, archive_sha256, config):
    # Make a patch object
    url = url_util.path_to_file_url(filename)
    s = Spec("patch").concretized()

    # make a stage
    with Stage(url) as stage:  # TODO: url isn't used; maybe refactor Stage
        stage.mirror_path = mock_patch_stage

        mkdirp(stage.source_path)
        with working_dir(stage.source_path):
            # write a file to be patched
            with open("foo.txt", "w") as f:
                f.write(
                    """\
first line
second line
"""
                )
            # save it for later comparison
            shutil.copyfile("foo.txt", "foo-original.txt")
            # write the expected result of patching.
            with open("foo-expected.txt", "w") as f:
                f.write(
                    """\
zeroth line
first line
third line
"""
                )
        # apply the patch and compare files
        patch = spack.patch.UrlPatch(s.package, url, sha256=sha256, archive_sha256=archive_sha256)
        with patch.stage:
            patch.stage.create()
            patch.stage.fetch()
            patch.stage.expand_archive()
            patch.apply(stage)

        with working_dir(stage.source_path):
            assert filecmp.cmp("foo.txt", "foo-expected.txt")

        # apply the patch in reverse and compare files
        patch = spack.patch.UrlPatch(
            s.package, url, sha256=sha256, archive_sha256=archive_sha256, reverse=True
        )
        with patch.stage:
            patch.stage.create()
            patch.stage.fetch()
            patch.stage.expand_archive()
            patch.apply(stage)

        with working_dir(stage.source_path):
            assert filecmp.cmp("foo.txt", "foo-original.txt")


def test_patch_in_spec(mock_packages, config):
    """Test whether patches in a package appear in the spec."""
    spec = Spec("patch")
    spec.concretize()
    assert "patches" in list(spec.variants.keys())

    # Here the order is bar, foo, baz. Note that MV variants order
    # lexicographically based on the hash, not on the position of the
    # patch directive.
    assert (bar_sha256, foo_sha256, baz_sha256) == spec.variants["patches"].value

    assert (foo_sha256, bar_sha256, baz_sha256) == tuple(
        spec.variants["patches"]._patches_in_order_of_appearance
    )


def test_patch_mixed_versions_subset_constraint(mock_packages, config):
    """If we have a package with mixed x.y and x.y.z versions, make sure that
    a patch applied to a version range of x.y.z versions is not applied to
    an x.y version.
    """
    spec1 = Spec("patch@1.0.1")
    spec1.concretize()
    assert biz_sha256 in spec1.variants["patches"].value

    spec2 = Spec("patch@=1.0")
    spec2.concretize()
    assert biz_sha256 not in spec2.variants["patches"].value


def test_patch_order(mock_packages, config):
    spec = Spec("dep-diamond-patch-top")
    spec.concretize()

    mid2_sha256 = (
        "mid21234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
        if sys.platform != "win32"
        else "mid21234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
    )
    mid1_sha256 = (
        "0b62284961dab49887e31319843431ee5b037382ac02c4fe436955abef11f094"
        if sys.platform != "win32"
        else "aeb16c4dec1087e39f2330542d59d9b456dd26d791338ae6d80b6ffd10c89dfa"
    )
    top_sha256 = (
        "f7de2947c64cb6435e15fb2bef359d1ed5f6356b2aebb7b20535e3772904e6db"
        if sys.platform != "win32"
        else "ff34cb21271d16dbf928374f610bb5dd593d293d311036ddae86c4846ff79070"
    )

    dep = spec["patch"]
    patch_order = dep.variants["patches"]._patches_in_order_of_appearance
    # 'mid2' comes after 'mid1' alphabetically
    # 'top' comes after 'mid1'/'mid2' alphabetically
    # 'patch' comes last of all specs in the dag, alphabetically, so the
    # patches of 'patch' to itself are applied last. The patches applied by
    # 'patch' are ordered based on their appearance in the package.py file
    expected_order = (mid1_sha256, mid2_sha256, top_sha256, foo_sha256, bar_sha256, baz_sha256)

    assert expected_order == tuple(patch_order)


def test_nested_directives(mock_packages):
    """Ensure pkg data structures are set up properly by nested directives."""
    # this ensures that the patch() directive results were removed
    # properly from the DirectiveMeta._directives_to_be_executed list
    patcher = spack.repo.PATH.get_pkg_class("patch-several-dependencies")
    assert len(patcher.patches) == 0

    # this ensures that results of dependency patches were properly added
    # to Dependency objects.
    deps_by_name = patcher.dependencies_by_name()

    libelf_dep = deps_by_name["libelf"][0]
    assert len(libelf_dep.patches) == 1
    assert len(libelf_dep.patches[Spec()]) == 1

    libdwarf_dep = deps_by_name["libdwarf"][0]
    assert len(libdwarf_dep.patches) == 2
    assert len(libdwarf_dep.patches[Spec()]) == 1
    assert len(libdwarf_dep.patches[Spec("@20111030")]) == 1

    fake_dep = deps_by_name["fake"][0]
    assert len(fake_dep.patches) == 1
    assert len(fake_dep.patches[Spec()]) == 2


@pytest.mark.not_on_windows("Test requires Autotools")
def test_patched_dependency(mock_packages, install_mockery, mock_fetch):
    """Test whether patched dependencies work."""
    spec = Spec("patch-a-dependency")
    spec.concretize()
    assert "patches" in list(spec["libelf"].variants.keys())

    # make sure the patch makes it into the dependency spec
    t_sha = (
        "c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8"
        if sys.platform != "win32"
        else "3c5b65abcd6a3b2c714dbf7c31ff65fe3748a1adc371f030c283007ca5534f11"
    )
    assert (t_sha,) == spec["libelf"].variants["patches"].value

    # make sure the patch in the dependent's directory is applied to the
    # dependency
    libelf = spec["libelf"]
    pkg = libelf.package
    pkg.do_patch()
    with pkg.stage:
        with working_dir(pkg.stage.source_path):
            # output a Makefile with 'echo Patched!' as the default target
            configure = Executable("./configure")
            configure()

            # Make sure the Makefile contains the patched text
            with open("Makefile") as mf:
                assert "Patched!" in mf.read()


def trigger_bad_patch(pkg):
    if not os.path.isdir(pkg.stage.source_path):
        os.makedirs(pkg.stage.source_path)
    bad_file = os.path.join(pkg.stage.source_path, ".spack_patch_failed")
    touch(bad_file)
    return bad_file


def test_patch_failure_develop_spec_exits_gracefully(
    mock_packages, install_mockery, mock_fetch, tmpdir, mock_stage
):
    """ensure that a failing patch does not trigger exceptions for develop specs"""

    spec = Spec(f"patch-a-dependency ^libelf dev_path={tmpdir}")
    spec.concretize()
    libelf = spec["libelf"]
    assert "patches" in list(libelf.variants.keys())
    pkg = libelf.package
    with pkg.stage:
        bad_patch_indicator = trigger_bad_patch(pkg)
        assert os.path.isfile(bad_patch_indicator)
        pkg.do_patch()
    # success if no exceptions raised


def test_patch_failure_restages(mock_packages, install_mockery, mock_fetch):
    """
    ensure that a failing patch does not trigger exceptions
    for non-develop specs and the source gets restaged
    """
    spec = Spec("patch-a-dependency")
    spec.concretize()
    pkg = spec["libelf"].package
    with pkg.stage:
        bad_patch_indicator = trigger_bad_patch(pkg)
        assert os.path.isfile(bad_patch_indicator)
        pkg.do_patch()
        assert not os.path.isfile(bad_patch_indicator)


def test_multiple_patched_dependencies(mock_packages, config):
    """Test whether multiple patched dependencies work."""
    spec = Spec("patch-several-dependencies")
    spec.concretize()

    # basic patch on libelf
    assert "patches" in list(spec["libelf"].variants.keys())
    # foo
    assert (foo_sha256,) == spec["libelf"].variants["patches"].value

    # URL patches
    assert "patches" in list(spec["fake"].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (url2_sha256, url1_sha256) == spec["fake"].variants["patches"].value


def test_conditional_patched_dependencies(mock_packages, config):
    """Test whether conditional patched dependencies work."""
    spec = Spec("patch-several-dependencies @1.0")
    spec.concretize()

    # basic patch on libelf
    assert "patches" in list(spec["libelf"].variants.keys())
    # foo
    assert (foo_sha256,) == spec["libelf"].variants["patches"].value

    # conditional patch on libdwarf
    assert "patches" in list(spec["libdwarf"].variants.keys())
    # bar
    assert (bar_sha256,) == spec["libdwarf"].variants["patches"].value
    # baz is conditional on libdwarf version
    assert baz_sha256 not in spec["libdwarf"].variants["patches"].value

    # URL patches
    assert "patches" in list(spec["fake"].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (url2_sha256, url1_sha256) == spec["fake"].variants["patches"].value


def check_multi_dependency_patch_specs(
    libelf, libdwarf, fake, owner, package_dir  # specs
):  # parent spec properties
    """Validate patches on dependencies of patch-several-dependencies."""
    # basic patch on libelf
    assert "patches" in list(libelf.variants.keys())
    # foo
    assert foo_sha256 in libelf.variants["patches"].value

    # conditional patch on libdwarf
    assert "patches" in list(libdwarf.variants.keys())
    # bar
    assert bar_sha256 in libdwarf.variants["patches"].value
    # baz is conditional on libdwarf version (no guarantee on order w/conds)
    assert baz_sha256 in libdwarf.variants["patches"].value

    def get_patch(spec, ending):
        return next(p for p in spec.patches if p.path_or_url.endswith(ending))

    # make sure file patches are reconstructed properly
    foo_patch = get_patch(libelf, "foo.patch")
    bar_patch = get_patch(libdwarf, "bar.patch")
    baz_patch = get_patch(libdwarf, "baz.patch")

    assert foo_patch.owner == owner
    assert foo_patch.path == os.path.join(package_dir, "foo.patch")
    assert foo_patch.sha256 == foo_sha256

    assert bar_patch.owner == "builtin.mock.patch-several-dependencies"
    assert bar_patch.path == os.path.join(package_dir, "bar.patch")
    assert bar_patch.sha256 == bar_sha256

    assert baz_patch.owner == "builtin.mock.patch-several-dependencies"
    assert baz_patch.path == os.path.join(package_dir, "baz.patch")
    assert baz_patch.sha256 == baz_sha256

    # URL patches
    assert "patches" in list(fake.variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (url2_sha256, url1_sha256) == fake.variants["patches"].value

    url1_patch = get_patch(fake, "urlpatch.patch")
    url2_patch = get_patch(fake, "urlpatch2.patch.gz")

    assert url1_patch.owner == "builtin.mock.patch-several-dependencies"
    assert url1_patch.url == "http://example.com/urlpatch.patch"
    assert url1_patch.sha256 == url1_sha256

    assert url2_patch.owner == "builtin.mock.patch-several-dependencies"
    assert url2_patch.url == "http://example.com/urlpatch2.patch.gz"
    assert url2_patch.sha256 == url2_sha256
    assert url2_patch.archive_sha256 == url2_archive_sha256


def test_conditional_patched_deps_with_conditions(mock_packages, config):
    """Test whether conditional patched dependencies with conditions work."""
    spec = Spec("patch-several-dependencies @1.0 ^libdwarf@20111030")
    spec.concretize()

    libelf = spec["libelf"]
    libdwarf = spec["libdwarf"]
    fake = spec["fake"]

    check_multi_dependency_patch_specs(
        libelf, libdwarf, fake, "builtin.mock.patch-several-dependencies", spec.package.package_dir
    )


def test_write_and_read_sub_dags_with_patched_deps(mock_packages, config):
    """Test whether patched dependencies are still correct after writing and
    reading a sub-DAG of a concretized Spec.
    """
    spec = Spec("patch-several-dependencies @1.0 ^libdwarf@20111030")
    spec.concretize()

    # write to YAML and read back in -- new specs will *only* contain
    # their sub-DAGs, and won't contain the dependent that patched them
    libelf = spack.spec.Spec.from_yaml(spec["libelf"].to_yaml())
    libdwarf = spack.spec.Spec.from_yaml(spec["libdwarf"].to_yaml())
    fake = spack.spec.Spec.from_yaml(spec["fake"].to_yaml())

    # make sure we can still read patches correctly for these specs
    check_multi_dependency_patch_specs(
        libelf, libdwarf, fake, "builtin.mock.patch-several-dependencies", spec.package.package_dir
    )


def test_patch_no_file():
    # Give it the attributes we need to construct the error message
    FakePackage = collections.namedtuple("FakePackage", ["name", "namespace", "fullname"])
    fp = FakePackage("fake-package", "test", "fake-package")
    with pytest.raises(ValueError, match="FilePatch:"):
        spack.patch.FilePatch(fp, "nonexistent_file", 0, "")

    patch = spack.patch.Patch(fp, "nonexistent_file", 0, "")
    patch.path = "test"
    with pytest.raises(spack.error.NoSuchPatchError, match="No such patch:"):
        patch.apply("")


def test_patch_no_sha256():
    # Give it the attributes we need to construct the error message
    FakePackage = collections.namedtuple("FakePackage", ["name", "namespace", "fullname"])
    fp = FakePackage("fake-package", "test", "fake-package")
    url = url_util.path_to_file_url("foo.tgz")
    match = "Compressed patches require 'archive_sha256' and patch 'sha256' attributes: file://"
    with pytest.raises(spack.error.PatchDirectiveError, match=match):
        spack.patch.UrlPatch(fp, url, sha256="", archive_sha256="")
    match = "URL patches require a sha256 checksum"
    with pytest.raises(spack.error.PatchDirectiveError, match=match):
        spack.patch.UrlPatch(fp, url, sha256="", archive_sha256="abc")


@pytest.mark.parametrize("level", [-1, 0.0, "1"])
def test_invalid_level(level):
    # Give it the attributes we need to construct the error message
    FakePackage = collections.namedtuple("FakePackage", ["name", "namespace"])
    fp = FakePackage("fake-package", "test")
    with pytest.raises(ValueError, match="Patch level needs to be a non-negative integer."):
        spack.patch.Patch(fp, "nonexistent_file", level, "")


def test_equality():
    FakePackage = collections.namedtuple("FakePackage", ["name", "namespace", "fullname"])
    fp = FakePackage("fake-package", "test", "fake-package")
    patch1 = spack.patch.UrlPatch(fp, "nonexistent_url1", sha256="abc")
    patch2 = spack.patch.UrlPatch(fp, "nonexistent_url2", sha256="def")
    assert patch1 == patch1
    assert patch1 != patch2
    assert patch1 != "not a patch"


def test_sha256_setter(mock_patch_stage, config):
    path = os.path.join(data_path, "foo.patch")
    s = Spec("patch").concretized()
    patch = spack.patch.FilePatch(s.package, path, level=1, working_dir=".")
    patch.sha256 = "abc"


def test_invalid_from_dict(mock_packages, config):
    dictionary = {}
    with pytest.raises(ValueError, match="Invalid patch dictionary:"):
        spack.patch.from_dict(dictionary)

    dictionary = {"owner": "patch"}
    with pytest.raises(ValueError, match="Invalid patch dictionary:"):
        spack.patch.from_dict(dictionary)

    dictionary = {
        "owner": "patch",
        "relative_path": "foo.patch",
        "level": 1,
        "working_dir": ".",
        "reverse": False,
        "sha256": bar_sha256,
    }
    with pytest.raises(spack.fetch_strategy.ChecksumError, match="sha256 checksum failed for"):
        spack.patch.from_dict(dictionary)
