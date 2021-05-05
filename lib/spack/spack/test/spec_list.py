# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest
import itertools
from spack.spec_list import SpecList
from spack.spec import Spec


class TestSpecList(object):
    default_input = ['mpileaks', '$mpis',
                     {'matrix': [['hypre'], ['$gccs', '$clangs']]},
                     'libelf']

    default_reference = {'gccs': SpecList('gccs', ['%gcc@4.5.0']),
                         'clangs': SpecList('clangs', ['%clang@3.3']),
                         'mpis': SpecList('mpis', ['zmpi@1.0', 'mpich@3.0'])}

    default_expansion = ['mpileaks', 'zmpi@1.0', 'mpich@3.0',
                         {'matrix': [
                             ['hypre'],
                             ['%gcc@4.5.0', '%clang@3.3'],
                         ]},
                         'libelf']

    default_constraints = [[Spec('mpileaks')],
                           [Spec('zmpi@1.0')],
                           [Spec('mpich@3.0')],
                           [Spec('hypre'), Spec('%gcc@4.5.0')],
                           [Spec('hypre'), Spec('%clang@3.3')],
                           [Spec('libelf')]]

    default_specs = [Spec('mpileaks'), Spec('zmpi@1.0'),
                     Spec('mpich@3.0'), Spec('hypre%gcc@4.5.0'),
                     Spec('hypre%clang@3.3'), Spec('libelf')]

    def test_spec_list_expansions(self):
        speclist = SpecList('specs', self.default_input,
                            self.default_reference)

        assert speclist.specs_as_yaml_list == self.default_expansion
        assert speclist.specs_as_constraints == self.default_constraints
        assert speclist.specs == self.default_specs

    def test_spec_list_constraint_ordering(self):
        specs = [{'matrix': [
            ['^zmpi'],
            ['%gcc@4.5.0'],
            ['hypre', 'libelf'],
            ['~shared'],
            ['cflags=-O3', 'cflags="-g -O0"'],
            ['^foo']
        ]}]

        speclist = SpecList('specs', specs)

        expected_specs = [
            Spec('hypre cflags=-O3 ~shared %gcc@4.5.0 ^foo ^zmpi'),
            Spec('hypre cflags="-g -O0" ~shared %gcc@4.5.0 ^foo ^zmpi'),
            Spec('libelf cflags=-O3 ~shared %gcc@4.5.0 ^foo ^zmpi'),
            Spec('libelf cflags="-g -O0" ~shared %gcc@4.5.0 ^foo ^zmpi'),
        ]
        assert speclist.specs == expected_specs

    def test_spec_list_add(self):
        speclist = SpecList('specs', self.default_input,
                            self.default_reference)

        assert speclist.specs_as_yaml_list == self.default_expansion
        assert speclist.specs_as_constraints == self.default_constraints
        assert speclist.specs == self.default_specs

        speclist.add('libdwarf')

        assert speclist.specs_as_yaml_list == self.default_expansion + [
            'libdwarf']
        assert speclist.specs_as_constraints == self.default_constraints + [
            [Spec('libdwarf')]]
        assert speclist.specs == self.default_specs + [Spec('libdwarf')]

    def test_spec_list_remove(self):
        speclist = SpecList('specs', self.default_input,
                            self.default_reference)

        assert speclist.specs_as_yaml_list == self.default_expansion
        assert speclist.specs_as_constraints == self.default_constraints
        assert speclist.specs == self.default_specs

        speclist.remove('libelf')

        assert speclist.specs_as_yaml_list + [
            'libelf'
        ] == self.default_expansion

        assert speclist.specs_as_constraints + [
            [Spec('libelf')]
        ] == self.default_constraints

        assert speclist.specs + [Spec('libelf')] == self.default_specs

    def test_spec_list_update_reference(self):
        speclist = SpecList('specs', self.default_input,
                            self.default_reference)

        assert speclist.specs_as_yaml_list == self.default_expansion
        assert speclist.specs_as_constraints == self.default_constraints
        assert speclist.specs == self.default_specs

        new_mpis = SpecList('mpis', self.default_reference['mpis'].yaml_list)
        new_mpis.add('mpich@3.3')
        new_reference = self.default_reference.copy()
        new_reference['mpis'] = new_mpis

        speclist.update_reference(new_reference)

        expansion = list(self.default_expansion)
        expansion.insert(3, 'mpich@3.3')
        constraints = list(self.default_constraints)
        constraints.insert(3, [Spec('mpich@3.3')])
        specs = list(self.default_specs)
        specs.insert(3, Spec('mpich@3.3'))

        assert speclist.specs_as_yaml_list == expansion
        assert speclist.specs_as_constraints == constraints
        assert speclist.specs == specs

    def test_spec_list_extension(self):
        speclist = SpecList('specs', self.default_input,
                            self.default_reference)

        assert speclist.specs_as_yaml_list == self.default_expansion
        assert speclist.specs_as_constraints == self.default_constraints
        assert speclist.specs == self.default_specs

        new_ref = self.default_reference.copy()
        otherlist = SpecList('specs',
                             ['zlib', {'matrix': [['callpath'],
                                                  ['%intel@18']]}],
                             new_ref)

        speclist.extend(otherlist)

        assert speclist.specs_as_yaml_list == (self.default_expansion +
                                               otherlist.specs_as_yaml_list)
        assert speclist.specs == self.default_specs + otherlist.specs
        assert speclist._reference is new_ref

    def test_spec_list_nested_matrices(self):
        inner_matrix = [{'matrix': [['zlib', 'libelf'], ['%gcc', '%intel']]}]
        outer_addition = ['+shared', '~shared']
        outer_matrix = [{'matrix': [inner_matrix, outer_addition]}]
        speclist = SpecList('specs', outer_matrix)

        expected_components = itertools.product(['zlib', 'libelf'],
                                                ['%gcc', '%intel'],
                                                ['+shared', '~shared'])
        expected = [Spec(' '.join(combo)) for combo in expected_components]
        assert set(speclist.specs) == set(expected)

    @pytest.mark.regression('16897')
    def test_spec_list_recursion_specs_as_constraints(self):
        input = ['mpileaks', '$mpis',
                 {'matrix': [['hypre'], ['$%gccs', '$%clangs']]},
                 'libelf']

        reference = {'gccs': SpecList('gccs', ['gcc@4.5.0']),
                     'clangs': SpecList('clangs', ['clang@3.3']),
                     'mpis': SpecList('mpis', ['zmpi@1.0', 'mpich@3.0'])}

        speclist = SpecList('specs', input, reference)

        assert speclist.specs_as_yaml_list == self.default_expansion
        assert speclist.specs_as_constraints == self.default_constraints
        assert speclist.specs == self.default_specs

    def test_spec_list_matrix_exclude(self, mock_packages):
        # Test on non-boolean variants for regression for #16841
        matrix = [{'matrix': [['multivalue-variant'], ['foo=bar', 'foo=baz']],
                   'exclude': ['foo=bar']}]
        speclist = SpecList('specs', matrix)
        assert len(speclist.specs) == 1

    @pytest.mark.regression('22991')
    def test_spec_list_constraints_with_structure(
            self, mock_packages, mock_fetch, install_mockery):
        # Setup by getting hash and installing package with dep
        libdwarf_spec = Spec('libdwarf').concretized()
        libdwarf_spec.package.do_install()

        # Create matrix
        matrix = {
            'matrix': [
                ['mpileaks'],
                ['^callpath'],
                ['^libdwarf/%s' % libdwarf_spec.dag_hash()]
            ]
        }

        # ensure the concrete spec was retained in the matrix entry of which
        # it is a dependency
        speclist = SpecList('specs', [matrix])
        assert len(speclist.specs) == 1
        assert libdwarf_spec in speclist.specs[0]
