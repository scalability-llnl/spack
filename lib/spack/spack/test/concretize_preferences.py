##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest

import spack
from spack.spec import Spec


@pytest.fixture()
def concretize_scope(config, tmpdir):
    """Adds a scope for concretization preferences"""
    tmpdir.ensure_dir('concretize')
    spack.config.ConfigScope(
        'concretize', str(tmpdir.join('concretize'))
    )
    yield
    # This is kind of weird, but that's how config scopes are
    # set in ConfigScope.__init__
    spack.config.config_scopes.pop('concretize')
    spack.pkgsort = spack.PreferredPackages()


def concretize(abstract_spec):
    return Spec(abstract_spec).concretized()


def update_packages(pkgname, section, value):
    """Update config and reread package list"""
    conf = {pkgname: {section: value}}
    spack.config.update_config('packages', conf, 'concretize')
    spack.pkgsort = spack.PreferredPackages()


def assert_variant_values(spec, **variants):
    concrete = concretize(spec)
    for variant, value in variants.items():
        assert concrete.variants[variant].value == value


@pytest.mark.usefixtures('concretize_scope', 'builtin_mock')
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

    def test_preferred_compilers(self, refresh_builtin_mock):
        """Test preferred compilers are applied correctly
        """
        update_packages('mpileaks', 'compiler', ['clang@3.3'])
        spec = concretize('mpileaks')
        assert spec.compiler == spack.spec.CompilerSpec('clang@3.3')

        update_packages('mpileaks', 'compiler', ['gcc@4.5.0'])
        spec = concretize('mpileaks')
        assert spec.compiler == spack.spec.CompilerSpec('gcc@4.5.0')

    def test_preferred_versions(self):
        """Test preferred package versions are applied correctly
        """
        update_packages('mpileaks', 'version', ['2.3'])
        spec = concretize('mpileaks')
        assert spec.version == spack.spec.Version('2.3')

        update_packages('mpileaks', 'version', ['2.2'])
        spec = concretize('mpileaks')
        assert spec.version == spack.spec.Version('2.2')

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

    def test_develop(self):
        """Test concretization with develop version"""
        spec = Spec('builtin.mock.develop-test')
        spec.concretize()
        assert spec.version == spack.spec.Version('0.2.15')
