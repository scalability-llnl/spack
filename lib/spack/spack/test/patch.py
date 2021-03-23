# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import filecmp
import pytest
import collections

from llnl.util.filesystem import working_dir, mkdirp

import spack.patch
import spack.paths
import spack.repo
import spack.util.compression
from spack.util.executable import Executable
from spack.stage import Stage
from spack.spec import Spec

# various sha256 sums (using variables for legibility)

# files with contents 'foo', 'bar', and 'baz'
foo_sha256 = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c'
bar_sha256 = '7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730'
baz_sha256 = 'bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c'
biz_sha256 = 'a69b288d7393261e613c276c6d38a01461028291f6e381623acc58139d01f54d'

# url patches
url1_sha256 = 'abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234'
url2_sha256 = '1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd'
url2_archive_sha256 = 'abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd'


@pytest.fixture()
def mock_patch_stage(tmpdir_factory, monkeypatch):
    # Don't disrupt the spack install directory with tests.
    mock_path = str(tmpdir_factory.mktemp('mock-patch-stage'))
    monkeypatch.setattr(spack.stage, '_stage_root', mock_path)
    return mock_path


data_path = os.path.join(spack.paths.test_path, 'data', 'patch')


@pytest.mark.parametrize('filename, sha256, archive_sha256', [
    # compressed patch -- needs sha256 and archive_256
    (os.path.join(data_path, 'foo.tgz'),
     '252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866',
     '4e8092a161ec6c3a1b5253176fcf33ce7ba23ee2ff27c75dbced589dabacd06e'),
    # uncompressed patch -- needs only sha256
    (os.path.join(data_path, 'foo.patch'),
     '252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866',
     None)
])
def test_url_patch(mock_patch_stage, filename, sha256, archive_sha256):
    # Make a patch object
    url = 'file://' + filename
    pkg = spack.repo.get('patch')
    patch = spack.patch.UrlPatch(
        pkg, url, sha256=sha256, archive_sha256=archive_sha256)

    # make a stage
    with Stage(url) as stage:  # TODO: url isn't used; maybe refactor Stage
        stage.mirror_path = mock_patch_stage

        mkdirp(stage.source_path)
        with working_dir(stage.source_path):
            # write a file to be patched
            with open('foo.txt', 'w') as f:
                f.write("""\
first line
second line
""")
            # write the expected result of patching.
            with open('foo-expected.txt', 'w') as f:
                f.write("""\
zeroth line
first line
third line
""")
        # apply the patch and compare files
        patch.fetch()
        patch.apply(stage)
        patch.clean()

        with working_dir(stage.source_path):
            assert filecmp.cmp('foo.txt', 'foo-expected.txt')


def test_patch_in_spec(mock_packages, config):
    """Test whether patches in a package appear in the spec."""
    spec = Spec('patch')
    spec.concretize()
    assert 'patches' in list(spec.variants.keys())

    # Here the order is bar, foo, baz. Note that MV variants order
    # lexicographically based on the hash, not on the position of the
    # patch directive.
    assert ((bar_sha256,
             foo_sha256,
             baz_sha256) ==
            spec.variants['patches'].value)

    assert ((foo_sha256, bar_sha256, baz_sha256) ==
            tuple(spec.variants['patches']._patches_in_order_of_appearance))


def test_patch_mixed_versions_subset_constraint(mock_packages, config):
    """If we have a package with mixed x.y and x.y.z versions, make sure that
       a patch applied to a version range of x.y.z versions is not applied to
       an x.y version.
    """
    spec1 = Spec('patch@1.0.1')
    spec1.concretize()
    assert biz_sha256 in spec1.variants['patches'].value

    spec2 = Spec('patch@1.0')
    spec2.concretize()
    assert biz_sha256 not in spec2.variants['patches'].value


def test_patch_order(mock_packages, config):
    spec = Spec('dep-diamond-patch-top')
    spec.concretize()

    mid2_sha256 = 'mid21234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234'
    mid1_sha256 = '0b62284961dab49887e31319843431ee5b037382ac02c4fe436955abef11f094'
    top_sha256 = 'f7de2947c64cb6435e15fb2bef359d1ed5f6356b2aebb7b20535e3772904e6db'

    dep = spec['patch']
    patch_order = dep.variants['patches']._patches_in_order_of_appearance
    # 'mid2' comes after 'mid1' alphabetically
    # 'top' comes after 'mid1'/'mid2' alphabetically
    # 'patch' comes last of all specs in the dag, alphabetically, so the
    # patches of 'patch' to itself are applied last. The patches applied by
    # 'patch' are ordered based on their appearance in the package.py file
    expected_order = (
        mid1_sha256,
        mid2_sha256,
        top_sha256,
        foo_sha256, bar_sha256, baz_sha256)

    assert expected_order == tuple(patch_order)


def test_nested_directives(mock_packages):
    """Ensure pkg data structures are set up properly by nested directives."""
    # this ensures that the patch() directive results were removed
    # properly from the DirectiveMeta._directives_to_be_executed list
    patcher = spack.repo.path.get_pkg_class('patch-several-dependencies')
    assert len(patcher.patches) == 0

    # this ensures that results of dependency patches were properly added
    # to Dependency objects.
    libelf_dep = next(iter(patcher.dependencies['libelf'].values()))
    assert len(libelf_dep.patches) == 1
    assert len(libelf_dep.patches[Spec()]) == 1

    libdwarf_dep = next(iter(patcher.dependencies['libdwarf'].values()))
    assert len(libdwarf_dep.patches) == 2
    assert len(libdwarf_dep.patches[Spec()]) == 1
    assert len(libdwarf_dep.patches[Spec('@20111030')]) == 1

    fake_dep = next(iter(patcher.dependencies['fake'].values()))
    assert len(fake_dep.patches) == 1
    assert len(fake_dep.patches[Spec()]) == 2


def test_patched_dependency(
        mock_packages, config, install_mockery, mock_fetch):
    """Test whether patched dependencies work."""
    spec = Spec('patch-a-dependency')
    spec.concretize()
    assert 'patches' in list(spec['libelf'].variants.keys())

    # make sure the patch makes it into the dependency spec
    assert (('c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8',) ==
            spec['libelf'].variants['patches'].value)

    # make sure the patch in the dependent's directory is applied to the
    # dependency
    libelf = spec['libelf']
    pkg = libelf.package
    pkg.do_patch()
    with pkg.stage:
        with working_dir(pkg.stage.source_path):
            # output a Makefile with 'echo Patched!' as the default target
            configure = Executable('./configure')
            configure()

            # Make sure the Makefile contains the patched text
            with open('Makefile') as mf:
                assert 'Patched!' in mf.read()


def test_multiple_patched_dependencies(mock_packages, config):
    """Test whether multiple patched dependencies work."""
    spec = Spec('patch-several-dependencies')
    spec.concretize()

    # basic patch on libelf
    assert 'patches' in list(spec['libelf'].variants.keys())
    # foo
    assert ((foo_sha256,) ==
            spec['libelf'].variants['patches'].value)

    # URL patches
    assert 'patches' in list(spec['fake'].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (
        (url2_sha256, url1_sha256) == spec['fake'].variants['patches'].value)


def test_conditional_patched_dependencies(mock_packages, config):
    """Test whether conditional patched dependencies work."""
    spec = Spec('patch-several-dependencies @1.0')
    spec.concretize()

    # basic patch on libelf
    assert 'patches' in list(spec['libelf'].variants.keys())
    # foo
    assert ((foo_sha256,) ==
            spec['libelf'].variants['patches'].value)

    # conditional patch on libdwarf
    assert 'patches' in list(spec['libdwarf'].variants.keys())
    # bar
    assert ((bar_sha256,) ==
            spec['libdwarf'].variants['patches'].value)
    # baz is conditional on libdwarf version
    assert (baz_sha256
            not in spec['libdwarf'].variants['patches'].value)

    # URL patches
    assert 'patches' in list(spec['fake'].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (
        (url2_sha256, url1_sha256) == spec['fake'].variants['patches'].value)


def check_multi_dependency_patch_specs(
        libelf, libdwarf, fake,  # specs
        owner, package_dir):     # parent spec properties
    """Validate patches on dependencies of patch-several-dependencies."""
    # basic patch on libelf
    assert 'patches' in list(libelf.variants.keys())
    # foo
    assert (foo_sha256 in libelf.variants['patches'].value)

    # conditional patch on libdwarf
    assert 'patches' in list(libdwarf.variants.keys())
    # bar
    assert (bar_sha256 in libdwarf.variants['patches'].value)
    # baz is conditional on libdwarf version (no guarantee on order w/conds)
    assert (baz_sha256 in libdwarf.variants['patches'].value)

    def get_patch(spec, ending):
        return next(p for p in spec.patches if p.path_or_url.endswith(ending))

    # make sure file patches are reconstructed properly
    foo_patch = get_patch(libelf, 'foo.patch')
    bar_patch = get_patch(libdwarf, 'bar.patch')
    baz_patch = get_patch(libdwarf, 'baz.patch')

    assert foo_patch.owner == owner
    assert foo_patch.path == os.path.join(package_dir, 'foo.patch')
    assert foo_patch.sha256 == foo_sha256

    assert bar_patch.owner == 'builtin.mock.patch-several-dependencies'
    assert bar_patch.path == os.path.join(package_dir, 'bar.patch')
    assert bar_patch.sha256 == bar_sha256

    assert baz_patch.owner == 'builtin.mock.patch-several-dependencies'
    assert baz_patch.path == os.path.join(package_dir, 'baz.patch')
    assert baz_patch.sha256 == baz_sha256

    # URL patches
    assert 'patches' in list(fake.variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (url2_sha256, url1_sha256) == fake.variants['patches'].value

    url1_patch = get_patch(fake, 'urlpatch.patch')
    url2_patch = get_patch(fake, 'urlpatch2.patch.gz')

    assert url1_patch.owner == 'builtin.mock.patch-several-dependencies'
    assert url1_patch.url == 'http://example.com/urlpatch.patch'
    assert url1_patch.sha256 == url1_sha256

    assert url2_patch.owner == 'builtin.mock.patch-several-dependencies'
    assert url2_patch.url == 'http://example.com/urlpatch2.patch.gz'
    assert url2_patch.sha256 == url2_sha256
    assert url2_patch.archive_sha256 == url2_archive_sha256


def test_conditional_patched_deps_with_conditions(mock_packages, config):
    """Test whether conditional patched dependencies with conditions work."""
    spec = Spec('patch-several-dependencies @1.0 ^libdwarf@20111030')
    spec.concretize()

    libelf = spec['libelf']
    libdwarf = spec['libdwarf']
    fake = spec['fake']

    check_multi_dependency_patch_specs(
        libelf, libdwarf, fake,
        'builtin.mock.patch-several-dependencies',
        spec.package.package_dir)


def test_write_and_read_sub_dags_with_patched_deps(mock_packages, config):
    """Test whether patched dependencies are still correct after writing and
       reading a sub-DAG of a concretized Spec.
    """
    spec = Spec('patch-several-dependencies @1.0 ^libdwarf@20111030')
    spec.concretize()

    # write to YAML and read back in -- new specs will *only* contain
    # their sub-DAGs, and won't contain the dependent that patched them
    libelf = spack.spec.Spec.from_yaml(spec['libelf'].to_yaml())
    libdwarf = spack.spec.Spec.from_yaml(spec['libdwarf'].to_yaml())
    fake = spack.spec.Spec.from_yaml(spec['fake'].to_yaml())

    # make sure we can still read patches correctly for these specs
    check_multi_dependency_patch_specs(
        libelf, libdwarf, fake,
        'builtin.mock.patch-several-dependencies',
        spec.package.package_dir)


def test_patch_no_file():
    # Give it the attributes we need to construct the error message
    FakePackage = collections.namedtuple(
        'FakePackage', ['name', 'namespace', 'fullname'])
    fp = FakePackage('fake-package', 'test', 'fake-package')
    with pytest.raises(ValueError, match='FilePatch:'):
        spack.patch.FilePatch(fp, 'nonexistent_file', 0, '')

    patch = spack.patch.Patch(fp, 'nonexistent_file', 0, '')
    patch.path = 'test'
    with pytest.raises(spack.patch.NoSuchPatchError, match='No such patch:'):
        patch.apply('')


@pytest.mark.parametrize('level', [-1, 0.0, '1'])
def test_invalid_level(level):
    # Give it the attributes we need to construct the error message
    FakePackage = collections.namedtuple('FakePackage', ['name', 'namespace'])
    fp = FakePackage('fake-package', 'test')
    with pytest.raises(ValueError,
                       match='Patch level needs to be a non-negative integer.'):
        spack.patch.Patch(fp, 'nonexistent_file', level, '')
