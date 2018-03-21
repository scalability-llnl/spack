##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import spack.architecture
import itertools
import pytest

from spack.spec import Spec, UnsatisfiableSpecError
from spack.spec import substitute_abstract_variants, parse_anonymous_spec
from spack.variant import InvalidVariantValueError
from spack.variant import MultipleValuesInExclusiveVariantError


def target_factory(spec_string, target_concrete):
    spec = Spec(spec_string)

    if target_concrete:
        spec._mark_concrete()
        substitute_abstract_variants(spec)

    return spec


def argument_factory(argument_spec, left):
    try:
        # If it's not anonymous, allow it
        right = target_factory(argument_spec, False)
    except Exception:
        right = parse_anonymous_spec(argument_spec, left.name)
    return right


def check_satisfies(target_spec, argument_spec, target_concrete=False):

    left = target_factory(target_spec, target_concrete)
    right = argument_factory(argument_spec, left)

    # Satisfies is one-directional.
    assert left.satisfies(right)
    assert left.satisfies(argument_spec)

    # If left satisfies right, then we should be able to constrain
    # right by left.  Reverse is not always true.
    right.copy().constrain(left)


def check_unsatisfiable(target_spec, argument_spec, target_concrete=False):

    left = target_factory(target_spec, target_concrete)
    right = argument_factory(argument_spec, left)

    assert not left.satisfies(right)
    assert not left.satisfies(argument_spec)

    with pytest.raises(UnsatisfiableSpecError):
        right.copy().constrain(left)


def check_constrain(expected, spec, constraint):
    exp = Spec(expected)
    spec = Spec(spec)
    constraint = Spec(constraint)
    spec.constrain(constraint)
    assert exp == spec


def check_constrain_changed(spec, constraint):
    spec = Spec(spec)
    assert spec.constrain(constraint)


def check_constrain_not_changed(spec, constraint):
    spec = Spec(spec)
    assert not spec.constrain(constraint)


def check_invalid_constraint(spec, constraint):
    spec = Spec(spec)
    constraint = Spec(constraint)
    with pytest.raises(UnsatisfiableSpecError):
        spec.constrain(constraint)


@pytest.mark.usefixtures('config', 'builtin_mock')
class TestSpecSematics(object):
    """This tests satisfies(), constrain() and other semantic operations
    on specs.
    """
    def test_satisfies(self):
        check_satisfies('libelf@0.8.13', '@0:1')
        check_satisfies('libdwarf^libelf@0.8.13', '^libelf@0:1')

    def test_satisfies_namespace(self):
        check_satisfies('builtin.mpich', 'mpich')
        check_satisfies('builtin.mock.mpich', 'mpich')

        # TODO: only works for deps now, but shouldn't we allow for root spec?
        # check_satisfies('builtin.mock.mpich', 'mpi')

        check_satisfies('builtin.mock.mpich', 'builtin.mock.mpich')

        check_unsatisfiable('builtin.mock.mpich', 'builtin.mpich')

    def test_satisfies_namespaced_dep(self):
        """Ensure spec from same or unspecified namespace satisfies namespace
           constraint."""
        check_satisfies('mpileaks ^builtin.mock.mpich', '^mpich')

        check_satisfies('mpileaks ^builtin.mock.mpich', '^mpi')
        check_satisfies(
            'mpileaks ^builtin.mock.mpich', '^builtin.mock.mpich')

        check_unsatisfiable(
            'mpileaks ^builtin.mock.mpich', '^builtin.mpich')

    def test_satisfies_compiler(self):
        check_satisfies('foo%gcc', '%gcc')
        check_satisfies('foo%intel', '%intel')
        check_unsatisfiable('foo%intel', '%gcc')
        check_unsatisfiable('foo%intel', '%pgi')

    def test_satisfies_compiler_version(self):
        check_satisfies('foo%gcc', '%gcc@4.7.2')
        check_satisfies('foo%intel', '%intel@4.7.2')

        check_satisfies('foo%pgi@4.5', '%pgi@4.4:4.6')
        check_satisfies('foo@2.0%pgi@4.5', '@1:3%pgi@4.4:4.6')

        check_unsatisfiable('foo%pgi@4.3', '%pgi@4.4:4.6')
        check_unsatisfiable('foo@4.0%pgi', '@1:3%pgi')
        check_unsatisfiable('foo@4.0%pgi@4.5', '@1:3%pgi@4.4:4.6')

        check_satisfies('foo %gcc@4.7.3', '%gcc@4.7')
        check_unsatisfiable('foo %gcc@4.7', '%gcc@4.7.3')

    def test_satisfies_architecture(self):
        check_satisfies(
            'foo platform=test',
            'platform=test')
        check_satisfies(
            'foo platform=linux',
            'platform=linux')
        check_satisfies(
            'foo platform=test',
            'platform=test target=frontend')
        check_satisfies(
            'foo platform=test',
            'platform=test os=frontend target=frontend')
        check_satisfies(
            'foo platform=test os=frontend target=frontend',
            'platform=test')

        check_unsatisfiable(
            'foo platform=linux',
            'platform=test os=redhat6 target=x86_32')
        check_unsatisfiable(
            'foo os=redhat6',
            'platform=test os=debian6 target=x86_64')
        check_unsatisfiable(
            'foo target=x86_64',
            'platform=test os=redhat6 target=x86_32')

        check_satisfies(
            'foo arch=test-None-None',
            'platform=test')
        check_satisfies(
            'foo arch=test-None-frontend',
            'platform=test target=frontend')
        check_satisfies(
            'foo arch=test-frontend-frontend',
            'platform=test os=frontend target=frontend')
        check_satisfies(
            'foo arch=test-frontend-frontend',
            'platform=test')
        check_unsatisfiable(
            'foo arch=test-frontend-frontend',
            'platform=test os=frontend target=backend')

        check_satisfies(
            'foo platform=test target=frontend os=frontend',
            'platform=test target=frontend os=frontend')
        check_satisfies(
            'foo platform=test target=backend os=backend',
            'platform=test target=backend os=backend')
        check_satisfies(
            'foo platform=test target=default_target os=default_os',
            'platform=test os=default_os')
        check_unsatisfiable(
            'foo platform=test target=x86_32 os=redhat6',
            'platform=linux target=x86_32 os=redhat6')

    def test_satisfies_dependencies(self):
        check_satisfies('mpileaks^mpich', '^mpich')
        check_satisfies('mpileaks^zmpi', '^zmpi')

        check_unsatisfiable('mpileaks^mpich', '^zmpi')
        check_unsatisfiable('mpileaks^zmpi', '^mpich')

    def test_satisfies_dependency_versions(self):
        check_satisfies('mpileaks^mpich@2.0', '^mpich@1:3')
        check_unsatisfiable('mpileaks^mpich@1.2', '^mpich@2.0')

        check_satisfies(
            'mpileaks^mpich@2.0^callpath@1.5', '^mpich@1:3^callpath@1.4:1.6')
        check_unsatisfiable(
            'mpileaks^mpich@4.0^callpath@1.5', '^mpich@1:3^callpath@1.4:1.6')
        check_unsatisfiable(
            'mpileaks^mpich@2.0^callpath@1.7', '^mpich@1:3^callpath@1.4:1.6')
        check_unsatisfiable(
            'mpileaks^mpich@4.0^callpath@1.7', '^mpich@1:3^callpath@1.4:1.6')

    def test_satisfies_virtual_dependencies(self):
        check_satisfies('mpileaks^mpi', '^mpi')
        check_satisfies('mpileaks^mpi', '^mpich')

        check_satisfies('mpileaks^mpi', '^zmpi')
        check_unsatisfiable('mpileaks^mpich', '^zmpi')

    def test_satisfies_virtual_dependency_versions(self):
        check_satisfies('mpileaks^mpi@1.5', '^mpi@1.2:1.6')
        check_unsatisfiable('mpileaks^mpi@3', '^mpi@1.2:1.6')

        check_satisfies('mpileaks^mpi@2:', '^mpich')
        check_satisfies('mpileaks^mpi@2:', '^mpich@3.0.4')
        check_satisfies('mpileaks^mpi@2:', '^mpich2@1.4')

        check_satisfies('mpileaks^mpi@1:', '^mpich2')
        check_satisfies('mpileaks^mpi@2:', '^mpich2')

        check_unsatisfiable('mpileaks^mpi@3:', '^mpich2@1.4')
        check_unsatisfiable('mpileaks^mpi@3:', '^mpich2')
        check_unsatisfiable('mpileaks^mpi@3:', '^mpich@1.0')

    def test_satisfies_matching_variant(self):
        check_satisfies('mpich+foo', 'mpich+foo')
        check_satisfies('mpich~foo', 'mpich~foo')
        check_satisfies('mpich foo=1', 'mpich foo=1')

        # confirm that synonymous syntax works correctly
        check_satisfies('mpich+foo', 'mpich foo=True')
        check_satisfies('mpich foo=true', 'mpich+foo')
        check_satisfies('mpich~foo', 'mpich foo=FALSE')
        check_satisfies('mpich foo=False', 'mpich~foo')

    def test_satisfies_multi_value_variant(self):
        # Check quoting
        check_satisfies('multivalue_variant foo="bar,baz"',
                        'multivalue_variant foo="bar,baz"')
        check_satisfies('multivalue_variant foo=bar,baz',
                        'multivalue_variant foo=bar,baz')
        check_satisfies('multivalue_variant foo="bar,baz"',
                        'multivalue_variant foo=bar,baz')

        # A more constrained spec satisfies a less constrained one
        check_satisfies('multivalue_variant foo="bar,baz"',
                        'multivalue_variant foo="bar"')

        check_satisfies('multivalue_variant foo="bar,baz"',
                        'multivalue_variant foo="baz"')

        check_satisfies('multivalue_variant foo="bar,baz,barbaz"',
                        'multivalue_variant foo="bar,baz"')

        check_satisfies('multivalue_variant foo="bar,baz"',
                        'foo="bar,baz"')

        check_satisfies('multivalue_variant foo="bar,baz"',
                        'foo="bar"')

    def test_satisfies_single_valued_variant(self):
        """Tests that the case reported in
        https://github.com/spack/spack/pull/2386#issuecomment-282147639
        is handled correctly.
        """
        a = Spec('a foobar=bar')
        a.concretize()

        assert a.satisfies('foobar=bar')

        # Assert that an autospec generated from a literal
        # gives the right result for a single valued variant
        assert 'foobar=bar' in a
        assert 'foobar=baz' not in a
        assert 'foobar=fee' not in a

        # ... and for a multi valued variant
        assert 'foo=bar' in a

        # Check that conditional dependencies are treated correctly
        assert '^b' in a

    def test_unsatisfied_single_valued_variant(self):
        a = Spec('a foobar=baz')
        a.concretize()
        assert '^b' not in a

        mv = Spec('multivalue_variant')
        mv.concretize()
        assert 'a@1.0' not in mv

    def test_indirect_unsatisfied_single_valued_variant(self):
        spec = Spec('singlevalue-variant-dependent')
        spec.concretize()
        assert 'a@1.0' not in spec

    def test_unsatisfiable_multi_value_variant(self):

        # Semantics for a multi-valued variant is different
        # Depending on whether the spec is concrete or not

        a = target_factory(
            'multivalue_variant foo="bar"', target_concrete=True
        )
        spec_str = 'multivalue_variant foo="bar,baz"'
        b = Spec(spec_str)
        assert not a.satisfies(b)
        assert not a.satisfies(spec_str)
        # A concrete spec cannot be constrained further
        with pytest.raises(UnsatisfiableSpecError):
            a.constrain(b)

        a = Spec('multivalue_variant foo="bar"')
        spec_str = 'multivalue_variant foo="bar,baz"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained
        assert a.satisfies(b)
        assert a.satisfies(spec_str)
        # An abstract spec can instead be constrained
        assert a.constrain(b)

        a = target_factory(
            'multivalue_variant foo="bar,baz"', target_concrete=True
        )
        spec_str = 'multivalue_variant foo="bar,baz,quux"'
        b = Spec(spec_str)
        assert not a.satisfies(b)
        assert not a.satisfies(spec_str)
        # A concrete spec cannot be constrained further
        with pytest.raises(UnsatisfiableSpecError):
            a.constrain(b)

        a = Spec('multivalue_variant foo="bar,baz"')
        spec_str = 'multivalue_variant foo="bar,baz,quux"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained
        assert a.satisfies(b)
        assert a.satisfies(spec_str)
        # An abstract spec can instead be constrained
        assert a.constrain(b)
        # ...but will fail during concretization if there are
        # values in the variant that are not allowed
        with pytest.raises(InvalidVariantValueError):
            a.concretize()

        # This time we'll try to set a single-valued variant
        a = Spec('multivalue_variant fee="bar"')
        spec_str = 'multivalue_variant fee="baz"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained,
        # as before concretization I don't know which type of variant
        # I have (if it is not a BV)
        assert a.satisfies(b)
        assert a.satisfies(spec_str)
        # A variant cannot be parsed as single-valued until we try to
        # concretize. This means that we can constrain the variant above
        assert a.constrain(b)
        # ...but will fail during concretization if there are
        # multiple values set
        with pytest.raises(MultipleValuesInExclusiveVariantError):
            a.concretize()

    def test_unsatisfiable_variant_types(self):
        # These should fail due to incompatible types

        # FIXME: these needs to be checked as the new relaxed
        # FIXME: semantic makes them fail (constrain does not raise)
        # check_unsatisfiable('multivalue_variant +foo',
        #                     'multivalue_variant foo="bar"')
        # check_unsatisfiable('multivalue_variant ~foo',
        #                     'multivalue_variant foo="bar"')

        check_unsatisfiable(
            target_spec='multivalue_variant foo="bar"',
            argument_spec='multivalue_variant +foo',
            target_concrete=True
        )

        check_unsatisfiable(
            target_spec='multivalue_variant foo="bar"',
            argument_spec='multivalue_variant ~foo',
            target_concrete=True
        )

    def test_satisfies_unconstrained_variant(self):
        # only asked for mpich, no constraints.  Either will do.
        check_satisfies('mpich+foo', 'mpich')
        check_satisfies('mpich~foo', 'mpich')
        check_satisfies('mpich foo=1', 'mpich')

    def test_unsatisfiable_variants(self):
        # This case is different depending on whether the specs are concrete.

        # 'mpich' is not concrete:
        check_satisfies('mpich', 'mpich+foo', False)
        check_satisfies('mpich', 'mpich~foo', False)
        check_satisfies('mpich', 'mpich foo=1', False)

        # 'mpich' is concrete:
        check_unsatisfiable('mpich', 'mpich+foo', True)
        check_unsatisfiable('mpich', 'mpich~foo', True)
        check_unsatisfiable('mpich', 'mpich foo=1', True)

    def test_unsatisfiable_variant_mismatch(self):
        # No matchi in specs
        check_unsatisfiable('mpich~foo', 'mpich+foo')
        check_unsatisfiable('mpich+foo', 'mpich~foo')
        check_unsatisfiable('mpich foo=True', 'mpich foo=False')

    def test_satisfies_matching_compiler_flag(self):
        check_satisfies('mpich cppflags="-O3"', 'mpich cppflags="-O3"')
        check_satisfies(
            'mpich cppflags="-O3 -Wall"', 'mpich cppflags="-O3 -Wall"'
        )

    def test_satisfies_unconstrained_compiler_flag(self):
        # only asked for mpich, no constraints.  Any will do.
        check_satisfies('mpich cppflags="-O3"', 'mpich')

    def test_unsatisfiable_compiler_flag(self):
        # This case is different depending on whether the specs are concrete.

        # 'mpich' is not concrete:
        check_satisfies('mpich', 'mpich cppflags="-O3"', False)

        # 'mpich' is concrete:
        check_unsatisfiable('mpich', 'mpich cppflags="-O3"', True)

    def test_copy_satisfies_transitive(self):
        spec = Spec('dttop')
        spec.concretize()
        copy = spec.copy()
        for s in itertools.chain([spec], spec.visible_dependencies()):
            assert s.satisfies(copy[s.name])
            assert copy[s.name].satisfies(s)

    def test_unsatisfiable_compiler_flag_mismatch(self):
        # No matchi in specs
        check_unsatisfiable(
            'mpich cppflags="-O3"', 'mpich cppflags="-O2"')

    def test_satisfies_virtual(self):
        # Don't use check_satisfies: it checks constrain() too, and
        # you can't constrain a non-virtual by a virtual.
        assert Spec('mpich').satisfies(Spec('mpi'))
        assert Spec('mpich2').satisfies(Spec('mpi'))
        assert Spec('zmpi').satisfies(Spec('mpi'))

    def test_satisfies_virtual_dep_with_virtual_constraint(self):
        """Ensure we can satisfy virtual constraints when there are multiple
           vdep providers in the specs."""
        assert Spec('netlib-lapack ^openblas').satisfies(
            'netlib-lapack ^openblas'
        )
        assert not Spec('netlib-lapack ^netlib-blas').satisfies(
            'netlib-lapack ^openblas'
        )
        assert not Spec('netlib-lapack ^openblas').satisfies(
            'netlib-lapack ^netlib-blas'
        )
        assert Spec('netlib-lapack ^netlib-blas').satisfies(
            'netlib-lapack ^netlib-blas'
        )

    def test_satisfies_same_spec_with_different_hash(self):
        """Ensure that concrete specs are matched *exactly* by hash."""
        s1 = Spec('mpileaks').concretized()
        s2 = s1.copy()

        assert s1.satisfies(s2)
        assert s2.satisfies(s1)

        # Simulate specs that were installed before and after a change to
        # Spack's hashing algorithm.  This just reverses s2's hash.
        s2._hash = s1.dag_hash()[-1::-1]

        assert not s1.satisfies(s2)
        assert not s2.satisfies(s1)

    # ========================================================================
    # Indexing specs
    # ========================================================================
    def test_self_index(self):
        s = Spec('callpath')
        assert s['callpath'] == s

    def test_dep_index(self):
        s = Spec('callpath')
        s.normalize()

        assert s['callpath'] == s
        assert type(s['dyninst']) == Spec
        assert type(s['libdwarf']) == Spec
        assert type(s['libelf']) == Spec
        assert type(s['mpi']) == Spec

        assert s['dyninst'].name == 'dyninst'
        assert s['libdwarf'].name == 'libdwarf'
        assert s['libelf'].name == 'libelf'
        assert s['mpi'].name == 'mpi'

    def test_spec_contains_deps(self):
        s = Spec('callpath')
        s.normalize()
        assert 'dyninst' in s
        assert 'libdwarf' in s
        assert 'libelf' in s
        assert 'mpi' in s

    @pytest.mark.usefixtures('config')
    def test_virtual_index(self):
        s = Spec('callpath')
        s.concretize()

        s_mpich = Spec('callpath ^mpich')
        s_mpich.concretize()

        s_mpich2 = Spec('callpath ^mpich2')
        s_mpich2.concretize()

        s_zmpi = Spec('callpath ^zmpi')
        s_zmpi.concretize()

        assert s['mpi'].name != 'mpi'
        assert s_mpich['mpi'].name == 'mpich'
        assert s_mpich2['mpi'].name == 'mpich2'
        assert s_zmpi['zmpi'].name == 'zmpi'

        for spec in [s, s_mpich, s_mpich2, s_zmpi]:
            assert 'mpi' in spec

    # ========================================================================
    # Constraints
    # ========================================================================
    def test_constrain_variants(self):
        check_constrain('libelf@2.1:2.5', 'libelf@0:2.5', 'libelf@2.1:3')
        check_constrain(
            'libelf@2.1:2.5%gcc@4.5:4.6',
            'libelf@0:2.5%gcc@2:4.6',
            'libelf@2.1:3%gcc@4.5:4.7'
        )
        check_constrain('libelf+debug+foo', 'libelf+debug', 'libelf+foo')
        check_constrain(
            'libelf+debug+foo', 'libelf+debug', 'libelf+debug+foo'
        )
        check_constrain(
            'libelf debug=2 foo=1', 'libelf debug=2', 'libelf foo=1'
        )
        check_constrain(
            'libelf debug=2 foo=1', 'libelf debug=2', 'libelf debug=2 foo=1'
        )

        check_constrain('libelf+debug~foo', 'libelf+debug', 'libelf~foo')
        check_constrain(
            'libelf+debug~foo', 'libelf+debug', 'libelf+debug~foo'
        )

    def test_constrain_multi_value_variant(self):
        check_constrain(
            'multivalue_variant foo="bar,baz"',
            'multivalue_variant foo="bar"',
            'multivalue_variant foo="baz"'
        )

        check_constrain(
            'multivalue_variant foo="bar,baz,barbaz"',
            'multivalue_variant foo="bar,barbaz"',
            'multivalue_variant foo="baz"'
        )

    def test_constrain_compiler_flags(self):
        check_constrain(
            'libelf cflags="-O3" cppflags="-Wall"',
            'libelf cflags="-O3"',
            'libelf cppflags="-Wall"'
        )
        check_constrain(
            'libelf cflags="-O3" cppflags="-Wall"',
            'libelf cflags="-O3"',
            'libelf cflags="-O3" cppflags="-Wall"'
        )

    def test_constrain_architecture(self):
        check_constrain(
            'libelf target=default_target os=default_os',
            'libelf target=default_target os=default_os',
            'libelf target=default_target os=default_os'
        )
        check_constrain(
            'libelf target=default_target os=default_os',
            'libelf',
            'libelf target=default_target os=default_os'
        )

    def test_constrain_compiler(self):
        check_constrain(
            'libelf %gcc@4.4.7', 'libelf %gcc@4.4.7', 'libelf %gcc@4.4.7'
        )
        check_constrain(
            'libelf %gcc@4.4.7', 'libelf', 'libelf %gcc@4.4.7'
        )

    def test_invalid_constraint(self):
        check_invalid_constraint('libelf@0:2.0', 'libelf@2.1:3')
        check_invalid_constraint(
            'libelf@0:2.5%gcc@4.8:4.9', 'libelf@2.1:3%gcc@4.5:4.7')

        check_invalid_constraint('libelf+debug', 'libelf~debug')
        check_invalid_constraint('libelf+debug~foo', 'libelf+debug+foo')
        check_invalid_constraint('libelf debug=True', 'libelf debug=False')

        check_invalid_constraint(
            'libelf cppflags="-O3"', 'libelf cppflags="-O2"')
        check_invalid_constraint(
            'libelf platform=test target=be os=be', 'libelf target=fe os=fe'
        )

    def test_constrain_changed(self):
        check_constrain_changed('libelf', '@1.0')
        check_constrain_changed('libelf', '@1.0:5.0')
        check_constrain_changed('libelf', '%gcc')
        check_constrain_changed('libelf%gcc', '%gcc@4.5')
        check_constrain_changed('libelf', '+debug')
        check_constrain_changed('libelf', '~debug')
        check_constrain_changed('libelf', 'debug=2')
        check_constrain_changed('libelf', 'cppflags="-O3"')

        platform = spack.architecture.platform()
        check_constrain_changed(
            'libelf', 'target=' + platform.target('default_target').name)
        check_constrain_changed(
            'libelf', 'os=' + platform.operating_system('default_os').name)

    def test_constrain_not_changed(self):
        check_constrain_not_changed('libelf', 'libelf')
        check_constrain_not_changed('libelf@1.0', '@1.0')
        check_constrain_not_changed('libelf@1.0:5.0', '@1.0:5.0')
        check_constrain_not_changed('libelf%gcc', '%gcc')
        check_constrain_not_changed('libelf%gcc@4.5', '%gcc@4.5')
        check_constrain_not_changed('libelf+debug', '+debug')
        check_constrain_not_changed('libelf~debug', '~debug')
        check_constrain_not_changed('libelf debug=2', 'debug=2')
        check_constrain_not_changed(
            'libelf cppflags="-O3"', 'cppflags="-O3"')

        platform = spack.architecture.platform()
        default_target = platform.target('default_target').name
        check_constrain_not_changed(
            'libelf target=' + default_target, 'target=' + default_target)

    def test_constrain_dependency_changed(self):
        check_constrain_changed('libelf^foo', 'libelf^foo@1.0')
        check_constrain_changed('libelf^foo', 'libelf^foo@1.0:5.0')
        check_constrain_changed('libelf^foo', 'libelf^foo%gcc')
        check_constrain_changed('libelf^foo%gcc', 'libelf^foo%gcc@4.5')
        check_constrain_changed('libelf^foo', 'libelf^foo+debug')
        check_constrain_changed('libelf^foo', 'libelf^foo~debug')

        platform = spack.architecture.platform()
        default_target = platform.target('default_target').name
        check_constrain_changed(
            'libelf^foo', 'libelf^foo target=' + default_target)

    def test_constrain_dependency_not_changed(self):
        check_constrain_not_changed('libelf^foo@1.0', 'libelf^foo@1.0')
        check_constrain_not_changed(
            'libelf^foo@1.0:5.0', 'libelf^foo@1.0:5.0')
        check_constrain_not_changed('libelf^foo%gcc', 'libelf^foo%gcc')
        check_constrain_not_changed(
            'libelf^foo%gcc@4.5', 'libelf^foo%gcc@4.5')
        check_constrain_not_changed(
            'libelf^foo+debug', 'libelf^foo+debug')
        check_constrain_not_changed(
            'libelf^foo~debug', 'libelf^foo~debug')
        check_constrain_not_changed(
            'libelf^foo cppflags="-O3"', 'libelf^foo cppflags="-O3"')

        platform = spack.architecture.platform()
        default_target = platform.target('default_target').name
        check_constrain_not_changed(
            'libelf^foo target=' + default_target,
            'libelf^foo target=' + default_target)

    def test_exceptional_paths_for_constructor(self):

        with pytest.raises(TypeError):
            Spec((1, 2))

        with pytest.raises(ValueError):
            Spec('')

        with pytest.raises(ValueError):
            Spec('libelf foo')
