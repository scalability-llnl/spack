# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import stat

import spack.package_prefs
import spack.repo
import spack.util.spack_yaml as syaml
from spack.config import ConfigScope, ConfigError
from spack.spec import Spec


@pytest.fixture()
def concretize_scope(config, tmpdir):
    """Adds a scope for concretization preferences"""
    tmpdir.ensure_dir('concretize')
    config.push_scope(
        ConfigScope('concretize', str(tmpdir.join('concretize'))))

    yield

    config.pop_scope()
    spack.package_prefs.PackagePrefs.clear_caches()
    spack.repo.path._provider_index = None


@pytest.fixture()
def configure_permissions():
    conf = syaml.load("""\
all:
  permissions:
    read: group
    write: group
    group: all
mpich:
  permissions:
    read: user
    write: user
mpileaks:
  permissions:
    write: user
    group: mpileaks
callpath:
  permissions:
    write: world
""")
    spack.config.set('packages', conf, scope='concretize')

    yield


def concretize(abstract_spec):
    return Spec(abstract_spec).concretized()


def update_packages(pkgname, section, value):
    """Update config and reread package list"""
    conf = {pkgname: {section: value}}
    spack.config.set('packages', conf, scope='concretize')
    spack.package_prefs.PackagePrefs.clear_caches()


def assert_variant_values(spec, **variants):
    concrete = concretize(spec)
    for variant, value in variants.items():
        assert concrete.variants[variant].value == value


@pytest.mark.usefixtures('concretize_scope', 'mock_packages')
class TestConcretizePreferences(object):
    def test_preferred_variants(self):
        """Test preferred variants are applied correctly
        """
        update_packages('mpileaks', 'variants', '~debug~opt+shared+static')
        assert_variant_values(
            'mpileaks', debug=False, opt=False, shared=True, static=True
        )
        update_packages(
            'mpileaks', 'variants', ['+debug', '+opt', '~shared', '-static']
        )
        assert_variant_values(
            'mpileaks', debug=True, opt=True, shared=False, static=False
        )

    def test_preferred_compilers(self, mutable_mock_packages):
        """Test preferred compilers are applied correctly
        """
        clang_spec = spack.spec.CompilerSpec('clang@3.3')
        gcc_spec = spack.spec.CompilerSpec('gcc@4.5.0')

        update_packages('mpileaks', 'compiler', ['clang@3.3'])
        spec = concretize('mpileaks')
        assert spec.compiler == clang_spec
        assert spec['callpath'].compiler == clang_spec
        assert spec['mpi'].compiler == clang_spec

        spec = concretize('mpileaks%gcc@4.5.0')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == gcc_spec
        assert spec['mpi'].compiler == gcc_spec

        update_packages('mpileaks', 'compiler', ['gcc@4.5.0'])
        spec = concretize('mpileaks')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == gcc_spec
        assert spec['mpi'].compiler == gcc_spec

        spec = concretize('mpileaks%clang@3.3')
        assert spec.compiler == clang_spec
        assert spec['callpath'].compiler == clang_spec
        assert spec['mpi'].compiler == clang_spec

        update_packages('all', 'compiler', ['clang@3.3'])
        spec = concretize('mpileaks')
        assert spec.compiler == clang_spec
        assert spec['callpath'].compiler == clang_spec
        assert spec['mpi'].compiler == clang_spec

        spec = concretize('mpileaks%gcc@4.5.0')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == gcc_spec
        assert spec['mpi'].compiler == gcc_spec

        update_packages('all', 'compiler', ['gcc@4.5.0'])
        spec = concretize('mpileaks')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == gcc_spec
        assert spec['mpi'].compiler == gcc_spec

        spec = concretize('mpileaks%clang@3.3')
        assert spec.compiler == clang_spec
        assert spec['callpath'].compiler == clang_spec
        assert spec['mpi'].compiler == clang_spec

        update_packages('callpath', 'compiler', ['clang@3.3'])
        spec = concretize('mpileaks')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == clang_spec
        assert spec['mpi'].compiler == gcc_spec

        spec = concretize('mpileaks%gcc@4.5.0')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == gcc_spec
        assert spec['mpi'].compiler == gcc_spec

        spec = concretize('mpileaks ^callpath%gcc@4.5.0')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == gcc_spec
        assert spec['mpi'].compiler == gcc_spec

        spec = concretize('mpileaks ^mpich%gcc@4.5.0')
        assert spec.compiler == gcc_spec
        assert spec['callpath'].compiler == clang_spec
        assert spec['mpi'].compiler == gcc_spec

    def test_preferred_versions(self):
        """Test preferred package versions are applied correctly
        """
        update_packages('mpileaks', 'version', ['2.3'])
        spec = concretize('mpileaks')
        assert spec.version == spack.spec.Version('2.3')

        update_packages('mpileaks', 'version', ['2.2'])
        spec = concretize('mpileaks')
        assert spec.version == spack.spec.Version('2.2')

    def test_preferred_versions_mixed_version_types(self):
        update_packages('mixedversions', 'version', ['2.0'])
        spec = concretize('mixedversions')
        assert spec.version == spack.spec.Version('2.0')

    def test_preferred_providers(self):
        """Test preferred providers of virtual packages are
        applied correctly
        """
        update_packages('all', 'providers', {'mpi': ['mpich']})
        spec = concretize('mpileaks')
        assert 'mpich' in spec

        update_packages('all', 'providers', {'mpi': ['zmpi']})
        spec = concretize('mpileaks')
        assert 'zmpi' in spec

    def test_preferred(self):
        """"Test packages with some version marked as preferred=True"""
        spec = Spec('preferred-test')
        spec.concretize()
        assert spec.version == spack.spec.Version('0.2.15')

        # now add packages.yaml with versions other than preferred
        # ensure that once config is in place, non-preferred version is used
        update_packages('preferred-test', 'version', ['0.2.16'])
        spec = Spec('preferred-test')
        spec.concretize()
        assert spec.version == spack.spec.Version('0.2.16')

    def test_develop(self):
        """Test concretization with develop-like versions"""
        spec = Spec('develop-test')
        spec.concretize()
        assert spec.version == spack.spec.Version('0.2.15')
        spec = Spec('develop-test2')
        spec.concretize()
        assert spec.version == spack.spec.Version('0.2.15')

        # now add packages.yaml with develop-like versions
        # ensure that once config is in place, develop-like version is used
        update_packages('develop-test', 'version', ['develop'])
        spec = Spec('develop-test')
        spec.concretize()
        assert spec.version == spack.spec.Version('develop')

        update_packages('develop-test2', 'version', ['0.2.15.develop'])
        spec = Spec('develop-test2')
        spec.concretize()
        assert spec.version == spack.spec.Version('0.2.15.develop')

    def test_no_virtuals_in_packages_yaml(self):
        """Verify that virtuals are not allowed in packages.yaml."""

        # set up a packages.yaml file with a vdep as a key.  We use
        # syaml.load here to make sure source lines in the config are
        # attached to parsed strings, as the error message uses them.
        conf = syaml.load("""\
mpi:
    paths:
      mpi-with-lapack@2.1: /path/to/lapack
""")
        spack.config.set('packages', conf, scope='concretize')

        # now when we get the packages.yaml config, there should be an error
        with pytest.raises(spack.package_prefs.VirtualInPackagesYAMLError):
            spack.package_prefs.get_packages_config()

    def test_all_is_not_a_virtual(self):
        """Verify that `all` is allowed in packages.yaml."""
        conf = syaml.load("""\
all:
        variants: [+mpi]
""")
        spack.config.set('packages', conf, scope='concretize')

        # should be no error for 'all':
        spack.package_prefs.PackagePrefs.clear_caches()
        spack.package_prefs.get_packages_config()

    def test_external_mpi(self):
        # make sure this doesn't give us an external first.
        spec = Spec('mpi')
        spec.concretize()
        assert not spec['mpi'].external

        # load config
        conf = syaml.load("""\
all:
    providers:
        mpi: [mpich]
mpich:
    buildable: false
    paths:
        mpich@3.0.4: /dummy/path
""")
        spack.config.set('packages', conf, scope='concretize')

        # ensure that once config is in place, external is used
        spec = Spec('mpi')
        spec.concretize()
        assert spec['mpich'].external_path == '/dummy/path'

    def test_config_permissions_from_all(self, configure_permissions):
        # Although these aren't strictly about concretization, they are
        # configured in the same file and therefore convenient to test here.
        # Make sure we can configure readable and writable

        # Test inheriting from 'all'
        spec = Spec('zmpi')
        perms = spack.package_prefs.get_package_permissions(spec)
        assert perms == stat.S_IRWXU | stat.S_IRWXG

        dir_perms = spack.package_prefs.get_package_dir_permissions(spec)
        assert dir_perms == stat.S_IRWXU | stat.S_IRWXG | stat.S_ISGID

        group = spack.package_prefs.get_package_group(spec)
        assert group == 'all'

    def test_config_permissions_from_package(self, configure_permissions):
        # Test overriding 'all'
        spec = Spec('mpich')
        perms = spack.package_prefs.get_package_permissions(spec)
        assert perms == stat.S_IRWXU

        dir_perms = spack.package_prefs.get_package_dir_permissions(spec)
        assert dir_perms == stat.S_IRWXU

        group = spack.package_prefs.get_package_group(spec)
        assert group == 'all'

    def test_config_permissions_differ_read_write(self, configure_permissions):
        # Test overriding group from 'all' and different readable/writable
        spec = Spec('mpileaks')
        perms = spack.package_prefs.get_package_permissions(spec)
        assert perms == stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP

        dir_perms = spack.package_prefs.get_package_dir_permissions(spec)
        expected = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISGID
        assert dir_perms == expected

        group = spack.package_prefs.get_package_group(spec)
        assert group == 'mpileaks'

    def test_config_perms_fail_write_gt_read(self, configure_permissions):
        # Test failure for writable more permissive than readable
        spec = Spec('callpath')
        with pytest.raises(ConfigError):
            spack.package_prefs.get_package_permissions(spec)
