# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import pytest

from spack.error import SpecError, UnsatisfiableSpecError
from spack.spec import UnconstrainableDependencySpecError
from spack.spec import Spec, SpecFormatSigilError, SpecFormatStringError
from spack.variant import InvalidVariantValueError, UnknownVariantError
from spack.variant import MultipleValuesInExclusiveVariantError
from spack.variant import substitute_abstract_variants

import spack.architecture
import spack.directives
import spack.error


def make_spec(spec_like, concrete):
    if isinstance(spec_like, Spec):
        return spec_like

    spec = Spec(spec_like)
    if concrete:
        spec._mark_concrete()
        substitute_abstract_variants(spec)
    return spec


def _specify(spec_like):
    if isinstance(spec_like, Spec):
        return spec_like

    return Spec(spec_like)


def check_satisfies(target_spec, constraint_spec, target_concrete=False):

    target = make_spec(target_spec, target_concrete)
    constraint = _specify(constraint_spec)

    # Satisfies is one-directional.
    assert target.satisfies(constraint)

    # If target satisfies constraint, then we should be able to constrain
    # constraint by target.  Reverse is not always true.
    constraint.copy().constrain(target)


def check_unsatisfiable(target_spec, constraint_spec, target_concrete=False):

    target = make_spec(target_spec, target_concrete)
    constraint = _specify(constraint_spec)

    assert not target.satisfies(constraint)

    with pytest.raises(UnsatisfiableSpecError):
        constraint.copy().constrain(target)


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
    with pytest.raises((UnsatisfiableSpecError,
                        UnconstrainableDependencySpecError)):
        spec.constrain(constraint)


@pytest.mark.usefixtures('config', 'mock_packages')
class TestSpecSematics(object):
    """This tests satisfies(), constrain() and other semantic operations
    on specs.
    """
    def test_satisfies(self):
        check_satisfies('libelf@0.8.13', '@0:1')
        check_satisfies('libdwarf^libelf@0.8.13', '^libelf@0:1')

    def test_empty_satisfies(self):
        # Basic satisfaction
        check_satisfies('libelf', Spec())
        check_satisfies('libdwarf', Spec())
        check_satisfies('%intel', Spec())
        check_satisfies('^mpi', Spec())
        check_satisfies('+debug', Spec())
        check_satisfies('@3:', Spec())

        # Concrete (strict) satisfaction
        check_satisfies('libelf', Spec(), True)
        check_satisfies('libdwarf', Spec(), True)
        check_satisfies('%intel', Spec(), True)
        check_satisfies('^mpi', Spec(), True)
        # TODO: Variants can't be called concrete while anonymous
        # check_satisfies('+debug', Spec(), True)
        check_satisfies('@3:', Spec(), True)

        # Reverse (non-strict) satisfaction
        check_satisfies(Spec(), 'libelf')
        check_satisfies(Spec(), 'libdwarf')
        check_satisfies(Spec(), '%intel')
        check_satisfies(Spec(), '^mpi')
        # TODO: Variant matching is auto-strict
        # we should rethink this
        # check_satisfies(Spec(), '+debug')
        check_satisfies(Spec(), '@3:')

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
            'platform=test os=redhat6 target=x86')
        check_unsatisfiable(
            'foo os=redhat6',
            'platform=test os=debian6 target=x86_64')
        check_unsatisfiable(
            'foo target=x86_64',
            'platform=test os=redhat6 target=x86')

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
            'foo platform=test target=x86 os=redhat6',
            'platform=linux target=x86 os=redhat6')

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
        check_satisfies('mpich foo=*', 'mpich~foo')
        check_satisfies('mpich +foo', 'mpich foo=*')

    def test_satisfies_multi_value_variant(self):
        # Check quoting
        check_satisfies('multivalue-variant foo="bar,baz"',
                        'multivalue-variant foo="bar,baz"')
        check_satisfies('multivalue-variant foo=bar,baz',
                        'multivalue-variant foo=bar,baz')
        check_satisfies('multivalue-variant foo="bar,baz"',
                        'multivalue-variant foo=bar,baz')

        # A more constrained spec satisfies a less constrained one
        check_satisfies('multivalue-variant foo="bar,baz"',
                        'multivalue-variant foo=*')

        check_satisfies('multivalue-variant foo=*',
                        'multivalue-variant foo="bar,baz"')

        check_satisfies('multivalue-variant foo="bar,baz"',
                        'multivalue-variant foo="bar"')

        check_satisfies('multivalue-variant foo="bar,baz"',
                        'multivalue-variant foo="baz"')

        check_satisfies('multivalue-variant foo="bar,baz,barbaz"',
                        'multivalue-variant foo="bar,baz"')

        check_satisfies('multivalue-variant foo="bar,baz"',
                        'foo="bar,baz"')

        check_satisfies('multivalue-variant foo="bar,baz"',
                        'foo="bar"')

    def test_satisfies_single_valued_variant(self):
        """Tests that the case reported in
        https://github.com/spack/spack/pull/2386#issuecomment-282147639
        is handled correctly.
        """
        a = Spec('a foobar=bar')
        a.concretize()

        assert a.satisfies('foobar=bar')
        assert a.satisfies('foobar=*')

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

        mv = Spec('multivalue-variant')
        mv.concretize()
        assert 'a@1.0' not in mv

    def test_indirect_unsatisfied_single_valued_variant(self):
        spec = Spec('singlevalue-variant-dependent')
        spec.concretize()
        assert 'a@1.0' not in spec

    def test_unsatisfiable_multi_value_variant(self):

        # Semantics for a multi-valued variant is different
        # Depending on whether the spec is concrete or not

        a = make_spec(
            'multivalue-variant foo="bar"', concrete=True
        )
        spec_str = 'multivalue-variant foo="bar,baz"'
        b = Spec(spec_str)
        assert not a.satisfies(b)
        assert not a.satisfies(spec_str)
        # A concrete spec cannot be constrained further
        with pytest.raises(UnsatisfiableSpecError):
            a.constrain(b)

        a = Spec('multivalue-variant foo="bar"')
        spec_str = 'multivalue-variant foo="bar,baz"'
        b = Spec(spec_str)
        # The specs are abstract and they **could** be constrained
        assert a.satisfies(b)
        assert a.satisfies(spec_str)
        # An abstract spec can instead be constrained
        assert a.constrain(b)

        a = make_spec(
            'multivalue-variant foo="bar,baz"', concrete=True
        )
        spec_str = 'multivalue-variant foo="bar,baz,quux"'
        b = Spec(spec_str)
        assert not a.satisfies(b)
        assert not a.satisfies(spec_str)
        # A concrete spec cannot be constrained further
        with pytest.raises(UnsatisfiableSpecError):
            a.constrain(b)

        a = Spec('multivalue-variant foo="bar,baz"')
        spec_str = 'multivalue-variant foo="bar,baz,quux"'
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
        a = Spec('multivalue-variant fee="bar"')
        spec_str = 'multivalue-variant fee="baz"'
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
        # check_unsatisfiable('multivalue-variant +foo',
        #                     'multivalue-variant foo="bar"')
        # check_unsatisfiable('multivalue-variant ~foo',
        #                     'multivalue-variant foo="bar"')

        check_unsatisfiable(
            target_spec='multivalue-variant foo="bar"',
            constraint_spec='multivalue-variant +foo',
            target_concrete=True
        )

        check_unsatisfiable(
            target_spec='multivalue-variant foo="bar"',
            constraint_spec='multivalue-variant ~foo',
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
        for s in spec.traverse():
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
            'multivalue-variant foo="bar,baz"',
            'multivalue-variant foo="bar"',
            'multivalue-variant foo="baz"'
        )

        check_constrain(
            'multivalue-variant foo="bar,baz,barbaz"',
            'multivalue-variant foo="bar,barbaz"',
            'multivalue-variant foo="baz"'
        )

        check_constrain(
            'libelf foo=bar,baz', 'libelf foo=bar,baz', 'libelf foo=*')
        check_constrain(
            'libelf foo=bar,baz', 'libelf foo=*', 'libelf foo=bar,baz')

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
        check_invalid_constraint('libdwarf', '^%gcc')

    def test_constrain_changed(self):
        check_constrain_changed('libelf', '@1.0')
        check_constrain_changed('libelf', '@1.0:5.0')
        check_constrain_changed('libelf', '%gcc')
        check_constrain_changed('libelf%gcc', '%gcc@4.5')
        check_constrain_changed('libelf', '+debug')
        check_constrain_changed('libelf', 'debug=*')
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
        check_constrain_not_changed('libelf debug=2', 'debug=*')
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
        check_constrain_changed('libelf', '^foo')

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

    def test_spec_formatting(self):
        spec = Spec("multivalue-variant cflags=-O2")
        spec.concretize()

        # Since the default is the full spec see if the string rep of
        # spec is the same as the output of spec.format()
        # ignoring whitespace (though should we?) and ignoring dependencies
        spec_string = str(spec)
        idx = spec_string.index(' ^')
        assert spec_string[:idx] == spec.format().strip()

        # Testing named strings ie {string} and whether we get
        # the correct component
        # Mixed case intentional to test both
        package_segments = [("{NAME}", "name"),
                            ("{VERSION}", "versions"),
                            ("{compiler}", "compiler"),
                            ("{compiler_flags}", "compiler_flags"),
                            ("{variants}", "variants"),
                            ("{architecture}", "architecture")]

        sigil_package_segments = [("{@VERSIONS}", '@' + str(spec.version)),
                                  ("{%compiler}", '%' + str(spec.compiler)),
                                  ("{arch=architecture}",
                                   ' arch=' + str(spec.architecture))]

        compiler_segments = [("{compiler.name}", "name"),
                             ("{compiler.version}", "versions")]

        sigil_compiler_segments = [("{%compiler.name}",
                                    '%' + spec.compiler.name),
                                   ("{@compiler.version}",
                                    '@' + str(spec.compiler.version))]

        architecture_segments = [("{architecture.platform}", "platform"),
                                 ("{architecture.os}", "os"),
                                 ("{architecture.target}", "target")]

        other_segments = [('{spack_root}', spack.paths.spack_root),
                          ('{spack_install}', spack.store.layout.root),
                          ('{hash:7}', spec.dag_hash(7)),
                          ('{/hash}', '/' + spec.dag_hash())]

        for named_str, prop in package_segments:
            expected = getattr(spec, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        for named_str, expected in sigil_package_segments:
            actual = spec.format(named_str)
            assert expected == actual

        compiler = spec.compiler
        for named_str, prop in compiler_segments:
            expected = getattr(compiler, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        for named_str, expected in sigil_compiler_segments:
            actual = spec.format(named_str)
            assert expected == actual

        arch = spec.architecture
        for named_str, prop in architecture_segments:
            expected = getattr(arch, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        for named_str, expected in other_segments:
            actual = spec.format(named_str)
            assert expected == actual

    def test_spec_formatting_escapes(self):
        spec = Spec('multivalue-variant cflags=-O2')
        spec.concretize()

        sigil_mismatches = [
            '{@name}',
            '{@version.concrete}',
            '{%compiler.version}',
            '{/hashd}',
            '{arch=architecture.os}'
        ]

        for fmt_str in sigil_mismatches:
            with pytest.raises(SpecFormatSigilError):
                spec.format(fmt_str)

        bad_formats = [
            r'{}',
            r'name}',
            r'\{name}',
            r'{name',
            r'{name\}',
            r'{_concrete}',
            r'{dag_hash}',
            r'{foo}',
            r'{+variants.debug}'
        ]

        for fmt_str in bad_formats:
            with pytest.raises(SpecFormatStringError):
                spec.format(fmt_str)

    def test_spec_deprecated_formatting(self):
        spec = Spec("libelf cflags=-O2")
        spec.concretize()

        # Since the default is the full spec see if the string rep of
        # spec is the same as the output of spec.format()
        # ignoring whitespace (though should we?)
        assert str(spec) == spec.format('$_$@$%@+$+$=').strip()

        # Testing named strings ie {string} and whether we get
        # the correct component
        # Mixed case intentional for testing both
        package_segments = [("${PACKAGE}", "name"),
                            ("${VERSION}", "versions"),
                            ("${compiler}", "compiler"),
                            ("${compilerflags}", "compiler_flags"),
                            ("${options}", "variants"),
                            ("${architecture}", "architecture")]

        compiler_segments = [("${compilername}", "name"),
                             ("${compilerver}", "versions")]

        architecture_segments = [("${PLATFORM}", "platform"),
                                 ("${OS}", "os"),
                                 ("${TARGET}", "target")]

        for named_str, prop in package_segments:
            expected = getattr(spec, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        compiler = spec.compiler
        for named_str, prop in compiler_segments:
            expected = getattr(compiler, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

        arch = spec.architecture
        for named_str, prop in architecture_segments:
            expected = getattr(arch, prop, "")
            actual = spec.format(named_str)
            assert str(expected) == actual

    @pytest.mark.regression('9908')
    def test_spec_flags_maintain_order(self):
        # Spack was assembling flags in a manner that could result in
        # different orderings for repeated concretizations of the same
        # spec and config
        spec_str = 'libelf %gcc@4.7.2 os=redhat6'
        for _ in range(25):
            s = Spec(spec_str).concretized()
            assert all(
                s.compiler_flags[x] == ['-O0', '-g']
                for x in ('cflags', 'cxxflags', 'fflags')
            )

    def test_combination_of_wildcard_or_none(self):
        # Test that using 'none' and another value raises
        with pytest.raises(spack.variant.InvalidVariantValueCombinationError):
            Spec('multivalue-variant foo=none,bar')

        # Test that using wildcard and another value raises
        with pytest.raises(spack.variant.InvalidVariantValueCombinationError):
            Spec('multivalue-variant foo=*,bar')

    @pytest.mark.skipif(
        sys.version_info[0] == 2, reason='__wrapped__ requires python 3'
    )
    def test_errors_in_variant_directive(self):
        variant = spack.directives.variant.__wrapped__

        class Pkg(object):
            name = 'PKG'

        # We can't use names that are reserved by Spack
        fn = variant('patches')
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert "The name 'patches' is reserved" in str(exc_info.value)

        # We can't have conflicting definitions for arguments
        fn = variant(
            'foo', values=spack.variant.any_combination_of('fee', 'foom'),
            default='bar'
        )
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert " it is handled by an attribute of the 'values' " \
               "argument" in str(exc_info.value)

        # We can't leave None as a default value
        fn = variant('foo', default=None)
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert "either a default was not explicitly set, or 'None' was used"\
               in str(exc_info.value)

        # We can't use an empty string as a default value
        fn = variant('foo', default='')
        with pytest.raises(spack.directives.DirectiveError) as exc_info:
            fn(Pkg())
        assert "the default cannot be an empty string" in str(exc_info.value)

    def test_abstract_spec_prefix_error(self):
        spec = Spec('libelf')

        with pytest.raises(SpecError):
            spec.prefix

    def test_forwarding_of_architecture_attributes(self):
        spec = Spec('libelf target=x86_64').concretized()

        # Check that we can still access each member through
        # the architecture attribute
        assert 'test' in spec.architecture
        assert 'debian' in spec.architecture
        assert 'x86_64' in spec.architecture

        # Check that we forward the platform and os attribute correctly
        assert spec.platform == 'test'
        assert spec.os == 'debian6'

        # Check that the target is also forwarded correctly and supports
        # all the operators we expect
        assert spec.target == 'x86_64'
        assert spec.target.family == 'x86_64'
        assert 'avx512' not in spec.target
        assert spec.target < 'broadwell'

    @pytest.mark.parametrize('transitive', [True, False])
    def test_splice(self, transitive):
        # Tests the new splice function in Spec using a somewhat simple case
        # with a variant with a conditional dependency.
        # TODO: Test being able to splice in different provider for a virtual.
        # Example: mvapich for mpich.
        spec = Spec('splice-t')
        dep = Spec('splice-h+foo')
        spec.concretize()
        dep.concretize()
        # Sanity checking that these are not the same thing.
        assert dep.dag_hash() != spec['splice-h'].dag_hash()
        assert dep.build_hash() != spec['splice-h'].build_hash()
        # Do the splice.
        out = spec.splice(dep, transitive)
        # Returned spec should still be concrete.
        assert out.concrete
        # Traverse the spec and assert that all dependencies are accounted for.
        for node in spec.traverse():
            assert node.name in out
        # If the splice worked, then the full hash of the spliced dep should
        # now match the full hash of the build spec of the dependency from the
        # returned spec.
        out_h_build = out['splice-h'].build_spec
        assert out_h_build.full_hash() == dep.full_hash()
        # Transitivity should determine whether the transitive dependency was
        # changed.
        expected_z = dep['splice-z'] if transitive else spec['splice-z']
        assert out['splice-z'].full_hash() == expected_z.full_hash()
        # Sanity check build spec of out should be the original spec.
        assert (out['splice-t'].build_spec.full_hash() ==
                spec['splice-t'].full_hash())
        # Finally, the spec should know it's been spliced:
        assert out.spliced

    @pytest.mark.parametrize('transitive', [True, False])
    def test_splice_input_unchanged(self, transitive):
        spec = Spec('splice-t').concretized()
        dep = Spec('splice-h+foo').concretized()
        orig_spec_hash = spec.full_hash()
        orig_dep_hash = dep.full_hash()
        spec.splice(dep, transitive)
        # Post-splice, dag hash should still be different; no changes should be
        # made to these specs.
        assert spec.full_hash() == orig_spec_hash
        assert dep.full_hash() == orig_dep_hash

    @pytest.mark.parametrize('transitive', [True, False])
    def test_splice_subsequent(self, transitive):
        spec = Spec('splice-t')
        dep = Spec('splice-h+foo')
        spec.concretize()
        dep.concretize()
        out = spec.splice(dep, transitive)
        # Now we attempt a second splice.
        dep = Spec('splice-z+bar')
        dep.concretize()
        # Transitivity shouldn't matter since Splice Z has no dependencies.
        out2 = out.splice(dep, transitive)
        assert out2.concrete
        assert out2['splice-z'].build_hash() != spec['splice-z'].build_hash()
        assert out2['splice-z'].build_hash() != out['splice-z'].build_hash()
        assert out2['splice-z'].full_hash() != spec['splice-z'].full_hash()
        assert out2['splice-z'].full_hash() != out['splice-z'].full_hash()
        assert (out2['splice-t'].build_spec.full_hash() ==
                spec['splice-t'].full_hash())
        assert out2.spliced

    @pytest.mark.parametrize('spec,constraint,expected_result', [
        ('libelf target=haswell', 'target=broadwell', False),
        ('libelf target=haswell', 'target=haswell', True),
        ('libelf target=haswell', 'target=x86_64:', True),
        ('libelf target=haswell', 'target=:haswell', True),
        ('libelf target=haswell', 'target=icelake,:nocona', False),
        ('libelf target=haswell', 'target=haswell,:nocona', True),
        # Check that a single target is not treated as the start
        # or the end of an open range
        ('libelf target=haswell', 'target=x86_64', False),
        ('libelf target=x86_64', 'target=haswell', False),
    ])
    @pytest.mark.regression('13111')
    def test_target_constraints(self, spec, constraint, expected_result):
        s = Spec(spec)
        assert s.satisfies(constraint) is expected_result

    @pytest.mark.regression('13124')
    def test_error_message_unknown_variant(self):
        s = Spec('mpileaks +unknown')
        with pytest.raises(UnknownVariantError, match=r'package has no such'):
            s.concretize()

    @pytest.mark.regression('18527')
    def test_satisfies_dependencies_ordered(self):
        d = Spec('zmpi ^fake')
        s = Spec('mpileaks')
        s._add_dependency(d, ())
        assert s.satisfies('mpileaks ^zmpi ^fake', strict=True)


@pytest.mark.regression('3887')
@pytest.mark.parametrize('spec_str', [
    'git', 'hdf5', 'py-flake8'
])
def test_is_extension_after_round_trip_to_dict(config, spec_str):
    # x is constructed directly from string, y from a
    # round-trip to dict representation
    x = Spec(spec_str)
    x.concretize()
    y = Spec.from_dict(x.to_dict())

    # Using 'y' since the round-trip make us lose build dependencies
    for d in y.traverse():
        assert x[d.name].package.is_extension == y[d.name].package.is_extension
