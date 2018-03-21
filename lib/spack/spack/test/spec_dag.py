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
"""
These tests check Spec DAG operations using dummy packages.
"""
import pytest
import spack
import spack.architecture
import spack.package

from spack.spec import Spec
from spack.dependency import all_deptypes, Dependency, canonical_deptype
from spack.test.conftest import MockPackage, MockPackageMultiRepo

from spack.test.concretize_preferences import concretize_scope  # NOQA: ignore=F401


def check_links(spec_to_check):
    for spec in spec_to_check.traverse():
        for dependent in spec.dependents():
            assert spec.name in dependent.dependencies_dict()

        for dependency in spec.dependencies():
            assert spec.name in dependency.dependents_dict()


@pytest.fixture()
def saved_deps():
    """Returns a dictionary to save the dependencies."""
    return {}


@pytest.fixture()
def set_dependency(saved_deps):
    """Returns a function that alters the dependency information
    for a package in the ``saved_deps`` fixture.
    """
    def _mock(pkg_name, spec, deptypes=all_deptypes):
        """Alters dependence information for a package.

        Adds a dependency on <spec> to pkg. Use this to mock up constraints.
        """
        spec = Spec(spec)
        # Save original dependencies before making any changes.
        pkg = spack.repo.get(pkg_name)
        if pkg_name not in saved_deps:
            saved_deps[pkg_name] = (pkg, pkg.dependencies.copy())

        cond = Spec(pkg.name)
        dependency = Dependency(pkg, spec, type=deptypes)
        pkg.dependencies[spec.name] = {cond: dependency}
    return _mock


@pytest.mark.usefixtures('config')
def test_sync_build_and_link_deps():
    """Test that all instances of v are constrained to be the same for the
following spec DAG::

        w
       /|
      y x
     /  |\
    v   p q
        |  \
        v   v

All deptypes are (link, build) except for x dependency on p, which is
build-only. Note that the y->v and p->v dependencies could use different
instances of v if it were not for the q->v dependency.

"""
    saved_repo = spack.repo

    default = ('build', 'link')

    v = MockPackage('v', [], [])
    # Adding a condition for q on v ensures that q's instance of v is not
    # created during the first pass of the concretization algorithm
    q_conditions = {v.name: {'q@2:': v.name}}
    q = MockPackage('q', [v], [default], q_conditions)
    p = MockPackage('p', [v], [default])
    x = MockPackage('x', [p, q], [('build',), default])
    y = MockPackage('y', [v], [default])
    w = MockPackage('w', [y, x], [default, default])

    mock_repo = MockPackageMultiRepo([v, q, p, x, y, w])
    try:
        spack.repo = mock_repo
        spec = Spec('w')
        spec.concretize()

        v_instances = [spec['y'].get_dependency('v').spec,
                       spec['x']['p'].get_dependency('v').spec,
                       spec['q'].get_dependency('v').spec]
        assert all(v_instances[0] is s for s in v_instances)
    finally:
        spack.repo = saved_repo


@pytest.mark.usefixtures('config')
def test_separate_build_deps():
    """Test that each instance of v is concretized separately in the
following spec DAG::

        w
       / \
      x   y
     / \   \
    v1  \   v3
         z
         |
         v2

All deptypes are (link, build) except for those on v.

"""
    saved_repo = spack.repo

    default = ('build', 'link')
    build_only = ('build',)

    v = MockPackage('v', [], [])

    z = MockPackage('z', [v], [build_only],
                    {v.name: {'z': 'v@2'}})
    x = MockPackage('x', [v, z], [build_only, default],
                    {v.name: {'x': 'v@1'}})

    y = MockPackage('y', [v], [build_only],
                    {v.name: {'y': 'v@3'}})

    w = MockPackage('w', [y, x], [default, default])

    mock_repo = MockPackageMultiRepo([v, w, x, y, z])
    try:
        spack.repo = mock_repo
        spec = Spec('w')
        spec.concretize()

        assert 'v@1' in spec['x']
        assert 'v@2' in spec['z']
        assert 'v@3' in spec['y']
    finally:
        spack.repo = saved_repo


@pytest.mark.usefixtures('config')
def test_user_mentioned_deptypes_are_preserved():
    """Test that when a user explicitly mentions a dependency as part of a
spec, that the deptypes are preserved for it. Given the following DAG::

      w
     /|
    z x
      |
      y

"""
    xy_deptypes = ('build',)
    wz_deptypes = ('build', 'link')
    wx_deptypes = ('link', 'run')

    y = MockPackage('y', [], [])
    z = MockPackage('z', [], [])
    x = MockPackage('x', [y], [xy_deptypes])
    w = MockPackage('w', [z, x], [wz_deptypes, wx_deptypes])

    mock_repo = MockPackageMultiRepo([w, x, y, z])
    saved_repo = spack.repo
    try:
        spack.repo = mock_repo
        spec = Spec('w ^x@2')
        spec.concretize()

        assert spec._dependencies['z'].deptypes == wz_deptypes
        assert spec._dependencies['x'].deptypes == wx_deptypes
        assert spec['x']._dependencies['y'].deptypes == xy_deptypes
    finally:
        spack.repo = saved_repo


@pytest.mark.usefixtures('config', 'concretize_scope')
def test_non_buildable_build_dep_is_external():
    """Test that x is concretized as an external when it is marked as
not-buildable in the following DAG::

    w
    |
    x
    |
    y

"""
    xy_deptypes = ('build', 'link')
    wx_deptypes = ('build',)

    y = MockPackage('y', [], [])
    x = MockPackage('x', [y], [xy_deptypes])
    w = MockPackage('w', [x], [wx_deptypes])

    mock_repo = MockPackageMultiRepo([w, x, y])
    saved_repo = spack.repo
    try:
        spack.repo = mock_repo

        conf = spack.util.spack_yaml.load("""\
x:
    buildable: false
    paths:
        x@2: /dummy/path
""")
        spack.config.update_config('packages', conf, 'concretize')

        spec = Spec('w')
        spec.concretize()

        assert spec['x'].external
    finally:
        spack.repo = saved_repo


@pytest.mark.usefixtures('config')
def test_test_deptype():
    """Ensure that test-only dependencies are only included for specified
packages in the following spec DAG::

        w
       /|
      x y
        |
        z

w->y deptypes are (link, build), w->x and y->z deptypes are (test)

"""
    saved_repo = spack.repo

    default = ('build', 'link')
    test_only = ('test',)

    x = MockPackage('x', [], [])
    z = MockPackage('z', [], [])
    y = MockPackage('y', [z], [test_only])
    w = MockPackage('w', [x, y], [test_only, default])

    mock_repo = MockPackageMultiRepo([w, x, y, z])
    try:
        spack.package_testing.test(w.name)
        spack.repo = mock_repo
        spec = Spec('w')
        spec.concretize()

        assert ('x' in spec)
        assert ('z' not in spec)
    finally:
        spack.repo = saved_repo
        spack.package_testing.clear()


@pytest.mark.usefixtures('refresh_builtin_mock')
class TestSpecDag(object):

    def test_conflicting_package_constraints(self, set_dependency):
        set_dependency('mpileaks', 'mpich@1.0')
        set_dependency('callpath', 'mpich@2.0')

        spec = Spec('mpileaks ^mpich ^callpath ^dyninst ^libelf ^libdwarf')

        # TODO: try to do something to show that the issue was with
        # TODO: the user's input or with package inconsistencies.
        with pytest.raises(spack.spec.UnsatisfiableVersionSpecError):
            spec.normalize()

    def test_preorder_node_traversal(self):
        dag = Spec('mpileaks ^zmpi')
        dag.normalize()

        names = ['mpileaks', 'callpath', 'dyninst', 'libdwarf', 'libelf',
                 'zmpi', 'fake']
        pairs = list(zip([0, 1, 2, 3, 4, 2, 3], names))

        traversal = dag.traverse()
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(depth=True)
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_preorder_edge_traversal(self):
        dag = Spec('mpileaks ^zmpi')
        dag.normalize()

        names = ['mpileaks', 'callpath', 'dyninst', 'libdwarf', 'libelf',
                 'libelf', 'zmpi', 'fake', 'zmpi']
        pairs = list(zip([0, 1, 2, 3, 4, 3, 2, 3, 1], names))

        traversal = dag.traverse(cover='edges')
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover='edges', depth=True)
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_preorder_path_traversal(self):
        dag = Spec('mpileaks ^zmpi')
        dag.normalize()

        names = ['mpileaks', 'callpath', 'dyninst', 'libdwarf', 'libelf',
                 'libelf', 'zmpi', 'fake', 'zmpi', 'fake']
        pairs = list(zip([0, 1, 2, 3, 4, 3, 2, 3, 1, 2], names))

        traversal = dag.traverse(cover='paths')
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover='paths', depth=True)
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_postorder_node_traversal(self):
        dag = Spec('mpileaks ^zmpi')
        dag.normalize()

        names = ['libelf', 'libdwarf', 'dyninst', 'fake', 'zmpi',
                 'callpath', 'mpileaks']
        pairs = list(zip([4, 3, 2, 3, 2, 1, 0], names))

        traversal = dag.traverse(order='post')
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(depth=True, order='post')
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_postorder_edge_traversal(self):
        dag = Spec('mpileaks ^zmpi')
        dag.normalize()

        names = ['libelf', 'libdwarf', 'libelf', 'dyninst', 'fake', 'zmpi',
                 'callpath', 'zmpi', 'mpileaks']
        pairs = list(zip([4, 3, 3, 2, 3, 2, 1, 1, 0], names))

        traversal = dag.traverse(cover='edges', order='post')
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover='edges', depth=True, order='post')
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_postorder_path_traversal(self):
        dag = Spec('mpileaks ^zmpi')
        dag.normalize()

        names = ['libelf', 'libdwarf', 'libelf', 'dyninst', 'fake', 'zmpi',
                 'callpath', 'fake', 'zmpi', 'mpileaks']
        pairs = list(zip([4, 3, 3, 2, 3, 2, 1, 2, 1, 0], names))

        traversal = dag.traverse(cover='paths', order='post')
        assert [x.name for x in traversal] == names

        traversal = dag.traverse(cover='paths', depth=True, order='post')
        assert [(x, y.name) for x, y in traversal] == pairs

    def test_normalize_twice(self):
        """Make sure normalize can be run twice on the same spec,
           and that it is idempotent."""
        spec = Spec('mpileaks')
        spec.normalize()
        n1 = spec.copy()

        spec.normalize()
        assert n1 == spec

    def test_normalize_a_lot(self):
        spec = Spec('mpileaks')
        spec.normalize()
        spec.normalize()
        spec.normalize()
        spec.normalize()

    def test_normalize_with_virtual_spec(self, ):
        dag = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'dyninst': {
                        'libdwarf': {'libelf': None},
                        'libelf': None
                    },
                    'mpi': None
                },
                'mpi': None
            }
        })
        dag.normalize()

        # make sure nothing with the same name occurs twice
        counts = {}
        for spec in dag.traverse(key=id):
            if spec.name not in counts:
                counts[spec.name] = 0
            counts[spec.name] += 1

        for name in counts:
            assert counts[name] == 1

    def test_dependents_and_dependencies_are_correct(self):
        spec = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'dyninst': {
                        'libdwarf': {'libelf': None},
                        'libelf': None
                    },
                    'mpi': None
                },
                'mpi': None
            }
        })

        check_links(spec)
        spec.normalize()
        check_links(spec)

    def test_unsatisfiable_version(self, set_dependency):
        set_dependency('mpileaks', 'mpich@1.0')
        spec = Spec('mpileaks ^mpich@2.0 ^callpath ^dyninst ^libelf ^libdwarf')
        with pytest.raises(spack.spec.UnsatisfiableVersionSpecError):
            spec.normalize()

    def test_unsatisfiable_compiler(self, set_dependency):
        set_dependency('mpileaks', 'mpich%gcc')
        spec = Spec('mpileaks ^mpich%intel ^callpath ^dyninst ^libelf'
                    ' ^libdwarf')
        with pytest.raises(spack.spec.UnsatisfiableCompilerSpecError):
            spec.normalize()

    def test_unsatisfiable_compiler_version(self, set_dependency):
        set_dependency('mpileaks', 'mpich%gcc@4.6')
        spec = Spec('mpileaks ^mpich%gcc@4.5 ^callpath ^dyninst ^libelf'
                    ' ^libdwarf')
        with pytest.raises(spack.spec.UnsatisfiableCompilerSpecError):
            spec.normalize()

    def test_unsatisfiable_architecture(self, set_dependency):
        set_dependency('mpileaks', 'mpich platform=test target=be')
        spec = Spec('mpileaks ^mpich platform=test target=fe ^callpath'
                    ' ^dyninst ^libelf ^libdwarf')
        with pytest.raises(spack.spec.UnsatisfiableArchitectureSpecError):
            spec.normalize()

    def test_invalid_dep(self):
        spec = Spec('libelf ^mpich')
        with pytest.raises(spack.spec.InvalidDependencyError):
            spec.concretize()

        spec = Spec('libelf ^libdwarf')
        with pytest.raises(spack.spec.InvalidDependencyError):
            spec.concretize()

        spec = Spec('mpich ^dyninst ^libelf')
        with pytest.raises(spack.spec.InvalidDependencyError):
            spec.concretize()

    def test_equal(self):
        # Different spec structures to test for equality
        flat = Spec.from_literal(
            {'mpileaks ^callpath ^libelf ^libdwarf': None}
        )

        flat_init = Spec.from_literal({
            'mpileaks': {
                'callpath': None,
                'libdwarf': None,
                'libelf': None
            }
        })

        flip_flat = Spec.from_literal({
            'mpileaks': {
                'libelf': None,
                'libdwarf': None,
                'callpath': None
            }
        })

        dag = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'libdwarf': {
                        'libelf': None
                    }
                }
            }
        })

        flip_dag = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'libelf': {
                        'libdwarf': None
                    }
                }
            }
        })

        # All these are equal to each other with regular ==
        specs = (flat, flat_init, flip_flat, dag, flip_dag)
        for lhs, rhs in zip(specs, specs):
            assert lhs == rhs
            assert str(lhs) == str(rhs)

        # Same DAGs constructed different ways are equal
        assert flat.eq_dag(flat_init)

        # order at same level does not matter -- (dep on same parent)
        assert flat.eq_dag(flip_flat)

        # DAGs should be unequal if nesting is different
        assert not flat.eq_dag(dag)
        assert not flat.eq_dag(flip_dag)
        assert not flip_flat.eq_dag(dag)
        assert not flip_flat.eq_dag(flip_dag)
        assert not dag.eq_dag(flip_dag)

    def test_normalize_mpileaks(self):
        # Spec parsed in from a string
        spec = Spec.from_literal({
            'mpileaks ^mpich ^callpath ^dyninst ^libelf@1.8.11 ^libdwarf': None
        })

        # What that spec should look like after parsing
        expected_flat = Spec.from_literal({
            'mpileaks': {
                'mpich': None,
                'callpath': None,
                'dyninst': None,
                'libelf@1.8.11': None,
                'libdwarf': None
            }
        })

        # What it should look like after normalization
        mpich = Spec('mpich')
        libelf = Spec('libelf@1.8.11')
        expected_normalized = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'dyninst': {
                        'libdwarf': {libelf: None},
                        libelf: None
                    },
                    mpich: None
                },
                mpich: None
            },
        })

        # Similar to normalized spec, but now with copies of the same
        # libelf node.  Normalization should result in a single unique
        # node for each package, so this is the wrong DAG.
        non_unique_nodes = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'dyninst': {
                        'libdwarf': {'libelf@1.8.11': None},
                        'libelf@1.8.11': None
                    },
                    mpich: None
                },
                mpich: None
            }
        }, normal=False)

        # All specs here should be equal under regular equality
        specs = (spec, expected_flat, expected_normalized, non_unique_nodes)
        for lhs, rhs in zip(specs, specs):
            assert lhs == rhs
            assert str(lhs) == str(rhs)

        # Test that equal and equal_dag are doing the right thing
        assert spec == expected_flat
        assert spec.eq_dag(expected_flat)

        # Normalized has different DAG structure, so NOT equal.
        assert spec != expected_normalized
        assert not spec.eq_dag(expected_normalized)

        # Again, different DAG structure so not equal.
        assert spec != non_unique_nodes
        assert not spec.eq_dag(non_unique_nodes)

        spec.normalize()

        # After normalizing, spec_dag_equal should match the normalized spec.
        assert spec != expected_flat
        assert not spec.eq_dag(expected_flat)

        # verify DAG structure without deptypes.
        assert spec.eq_dag(expected_normalized, deptypes=False)
        assert not spec.eq_dag(non_unique_nodes, deptypes=False)

        assert not spec.eq_dag(expected_normalized, deptypes=True)
        assert not spec.eq_dag(non_unique_nodes, deptypes=True)

    def test_normalize_with_virtual_package(self):
        spec = Spec('mpileaks ^mpi ^libelf@1.8.11 ^libdwarf')
        spec.normalize()

        expected_normalized = Spec.from_literal({
            'mpileaks': {
                'callpath': {
                    'dyninst': {
                        'libdwarf': {'libelf@1.8.11': None},
                        'libelf@1.8.11': None
                    },
                    'mpi': None
                },
                'mpi': None
            }
        })

        assert str(spec) == str(expected_normalized)

    def test_contains(self):
        spec = Spec('mpileaks ^mpi ^libelf@1.8.11 ^libdwarf')
        assert Spec('mpi') in spec
        assert Spec('libelf') in spec
        assert Spec('libelf@1.8.11') in spec
        assert Spec('libelf@1.8.12') not in spec
        assert Spec('libdwarf') in spec
        assert Spec('libgoblin') not in spec
        assert Spec('mpileaks') in spec

    def test_copy_simple(self):
        orig = Spec('mpileaks')
        copy = orig.copy()
        check_links(copy)

        assert orig == copy
        assert orig.eq_dag(copy)
        assert orig._normal == copy._normal
        assert orig._concrete == copy._concrete

        # ensure no shared nodes bt/w orig and copy.
        orig_ids = set(id(s) for s in orig.traverse())
        copy_ids = set(id(s) for s in copy.traverse())
        assert not orig_ids.intersection(copy_ids)

    def test_copy_normalized(self):
        orig = Spec('mpileaks')
        orig.normalize()
        copy = orig.copy()
        check_links(copy)

        assert orig == copy
        assert orig.eq_dag(copy)
        assert orig._normal == copy._normal
        assert orig._concrete == copy._concrete

        # ensure no shared nodes bt/w orig and copy.
        orig_ids = set(id(s) for s in orig.traverse())
        copy_ids = set(id(s) for s in copy.traverse())
        assert not orig_ids.intersection(copy_ids)

    @pytest.mark.usefixtures('config')
    def test_copy_concretized(self):
        orig = Spec('mpileaks')
        orig.concretize()
        copy = orig.copy()

        check_links(copy)

        assert orig == copy
        assert orig.eq_dag(copy)
        assert orig._normal == copy._normal
        assert orig._concrete == copy._concrete

        # ensure no shared nodes bt/w orig and copy.
        orig_ids = set(id(s) for s in orig.traverse())
        copy_ids = set(id(s) for s in copy.traverse())
        assert not orig_ids.intersection(copy_ids)

    """
    Here is the graph with deptypes labeled (assume all packages have a 'dt'
    prefix). Arrows are marked with the deptypes ('b' for 'build', 'l' for
    'link', 'r' for 'run').

        use -bl-> top

        top -b->  build1
        top -bl-> link1
        top -r->  run1

        build1 -b->  build2
        build1 -bl-> link2
        build1 -r->  run2

        link1 -bl-> link3

        run1 -bl-> link5
        run1 -r->  run3

        link3 -b->  build2
        link3 -bl-> link4

        run3 -b-> build3
    """
    @pytest.mark.usefixtures('config')
    def test_deptype_traversal(self):
        dag = Spec('dtuse')
        dag.concretize()

        names = ['dtuse', 'dttop', 'dtbuild1', 'dtbuild2', 'dtlink2',
                 'dtlink1', 'dtlink3', 'dtbuild2', 'dtlink4']

        traversal = dag.traverse(deptype=('build', 'link'))
        assert [x.name for x in traversal] == names

    def test_deptype_traversal_with_builddeps(self):
        dag = Spec('dttop')
        dag.concretize()

        names = ['dttop', 'dtbuild1', 'dtbuild2', 'dtlink2',
                 'dtlink1', 'dtlink3', 'dtbuild2', 'dtlink4']

        traversal = dag.traverse(deptype=('build', 'link'))
        assert [x.name for x in traversal] == names

    def test_deptype_traversal_full(self):
        dag = Spec('dttop')
        dag.concretize()

        names = ['dttop', 'dtbuild1', 'dtbuild2', 'dtlink2', 'dtrun2',
                 'dtlink1', 'dtlink3', 'dtbuild2', 'dtlink4', 'dtrun1',
                 'dtlink5', 'dtrun3', 'dtbuild3']

        traversal = dag.traverse(deptype=all)
        assert [x.name for x in traversal] == names

    def test_deptype_traversal_run(self):
        dag = Spec('dttop')
        dag.normalize()

        names = ['dttop', 'dtrun1', 'dtrun3']

        traversal = dag.traverse(deptype='run')
        assert [x.name for x in traversal] == names

    def test_hash_bits(self):
        """Ensure getting first n bits of a base32-encoded DAG hash works."""

        # RFC 4648 base32 decode table
        b32 = dict((j, i) for i, j in enumerate('abcdefghijklmnopqrstuvwxyz'))
        b32.update(dict((j, i) for i, j in enumerate('234567', 26)))

        # some package hashes
        tests = [
            '35orsd4cenv743hg4i5vxha2lzayycby',
            '6kfqtj7dap3773rxog6kkmoweix5gpwo',
            'e6h6ff3uvmjbq3azik2ckr6ckwm3depv',
            'snz2juf4ij7sv77cq3vs467q6acftmur',
            '4eg47oedi5bbkhpoxw26v3oe6vamkfd7',
            'vrwabwj6umeb5vjw6flx2rnft3j457rw']

        for test_hash in tests:
            # string containing raw bits of hash ('1' and '0')
            expected = ''.join([format(b32[c], '#07b').replace('0b', '')
                                for c in test_hash])

            for bits in (1, 2, 3, 4, 7, 8, 9, 16, 64, 117, 128, 160):
                actual_int = spack.spec.base32_prefix_bits(test_hash, bits)
                fmt = "#0%sb" % (bits + 2)
                actual = format(actual_int, fmt).replace('0b', '')

                assert expected[:bits] == actual

            with pytest.raises(ValueError):
                spack.spec.base32_prefix_bits(test_hash, 161)

            with pytest.raises(ValueError):
                spack.spec.base32_prefix_bits(test_hash, 256)

    def test_traversal_directions(self):
        """Make sure child and parent traversals of specs work."""
        # Mock spec - d is used for a diamond dependency
        spec = Spec.from_literal({
            'a': {
                'b': {
                    'c': {'d': None},
                    'e': None
                },
                'f': {
                    'g': {'d': None}
                }
            }
        })

        assert (
            ['a', 'b', 'c', 'd', 'e', 'f', 'g'] ==
            [s.name for s in spec.traverse(direction='children')])

        assert (
            ['g', 'f', 'a'] ==
            [s.name for s in spec['g'].traverse(direction='parents')])

        assert (
            ['d', 'c', 'b', 'a', 'g', 'f'] ==
            [s.name for s in spec['d'].traverse(direction='parents')])

    def test_edge_traversals(self):
        """Make sure child and parent traversals of specs work."""
        # Mock spec - d is used for a diamond dependency
        spec = Spec.from_literal({
            'a': {
                'b': {
                    'c': {'d': None},
                    'e': None
                },
                'f': {
                    'g': {'d': None}
                }
            }
        })

        assert (
            ['a', 'b', 'c', 'd', 'e', 'f', 'g'] ==
            [s.name for s in spec.traverse(direction='children')])

        assert (
            ['g', 'f', 'a'] ==
            [s.name for s in spec['g'].traverse(direction='parents')])

        assert (
            ['d', 'c', 'b', 'a', 'g', 'f'] ==
            [s.name for s in spec['d'].traverse(direction='parents')])

    def test_copy_dependencies(self):
        s1 = Spec('mpileaks ^mpich2@1.1')
        s2 = s1.copy()

        assert '^mpich2@1.1' in s2
        assert '^mpich2' in s2

    def test_construct_spec_with_deptypes(self):
        """Ensure that it is possible to construct a spec with explicit
           dependency types."""
        s = Spec.from_literal({
            'a': {
                'b': {'c:build': None},
                'd': {
                    'e:build,link': {'f:run': None}
                }
            }
        })

        assert s['b']._dependencies['c'].deptypes == ('build',)
        assert s['d']._dependencies['e'].deptypes == ('build', 'link')
        assert s['e']._dependencies['f'].deptypes == ('run',)

        c_spec = s['b']._dependencies['c'].spec
        assert c_spec._dependents['b'].deptypes == ('build',)
        assert s['e']._dependents['d'].deptypes == ('build', 'link')
        assert s['f']._dependents['e'].deptypes == ('run',)

    def check_diamond_deptypes(self, spec):
        """Validate deptypes in dt-diamond spec.

        This ensures that concretization works properly when two packages
        depend on the same dependency in different ways.

        """
        assert spec['dt-diamond']._dependencies[
            'dt-diamond-left'].deptypes == ('build', 'link')

        assert spec['dt-diamond']._dependencies[
            'dt-diamond-right'].deptypes == ('build', 'link')

        assert spec['dt-diamond-left']._dependencies[
            'dt-diamond-bottom'].deptypes == ('build', 'link')

        assert spec['dt-diamond-right'] ._dependencies[
            'dt-diamond-bottom'].deptypes == ('build', 'link', 'run')

    def check_diamond_normalized_dag(self, spec):
        dag = Spec.from_literal({
            'dt-diamond': {
                'dt-diamond-left:build,link': {
                    'dt-diamond-bottom:build,link': None
                },
                'dt-diamond-right:build,link': {
                    'dt-diamond-bottom:build,link,run': None
                },

            }
        })

        assert spec.eq_dag(dag)

    def test_normalize_diamond_deptypes(self):
        """Ensure that dependency types are preserved even if the same thing is
           depended on in two different ways."""
        s = Spec('dt-diamond')
        s.normalize()

        self.check_diamond_deptypes(s)
        self.check_diamond_normalized_dag(s)

    def test_concretize_deptypes(self):
        """Ensure that dependency types are preserved after concretization."""
        s = Spec('dt-diamond')
        s.concretize()
        self.check_diamond_deptypes(s)

    def test_copy_deptypes(self):
        """Ensure that dependency types are preserved by spec copy."""
        s1 = Spec('dt-diamond')
        s1.normalize()
        self.check_diamond_deptypes(s1)
        self.check_diamond_normalized_dag(s1)

        s2 = s1.copy()
        self.check_diamond_normalized_dag(s2)
        self.check_diamond_deptypes(s2)

        s3 = Spec('dt-diamond')
        s3.concretize()
        self.check_diamond_deptypes(s3)

        s4 = s3.copy()
        self.check_diamond_deptypes(s4)

    def test_getitem_query(self):
        s = Spec('mpileaks')
        s.concretize()

        # Check a query to a non-virtual package
        a = s['callpath']

        query = a.last_query
        assert query.name == 'callpath'
        assert len(query.extra_parameters) == 0
        assert not query.isvirtual

        # Check a query to a virtual package
        a = s['mpi']

        query = a.last_query
        assert query.name == 'mpi'
        assert len(query.extra_parameters) == 0
        assert query.isvirtual

        # Check a query to a virtual package with
        # extra parameters after query
        a = s['mpi:cxx,fortran']

        query = a.last_query
        assert query.name == 'mpi'
        assert len(query.extra_parameters) == 2
        assert 'cxx' in query.extra_parameters
        assert 'fortran' in query.extra_parameters
        assert query.isvirtual

    def test_getitem_exceptional_paths(self):
        s = Spec('mpileaks')
        s.concretize()
        # Needed to get a proxy object
        q = s['mpileaks']

        # Test that the attribute is read-only
        with pytest.raises(AttributeError):
            q.libs = 'foo'

        with pytest.raises(AttributeError):
            q.libs

    def test_canonical_deptype(self):
        # special values
        assert canonical_deptype(all) == all_deptypes
        assert canonical_deptype('all') == all_deptypes

        with pytest.raises(ValueError):
            canonical_deptype(None)
        with pytest.raises(ValueError):
            canonical_deptype([None])

        # everything in all_deptypes is canonical
        for v in all_deptypes:
            assert canonical_deptype(v) == (v,)

        # tuples
        assert canonical_deptype(('build',)) == ('build',)
        assert canonical_deptype(
            ('build', 'link', 'run')) == ('build', 'link', 'run')
        assert canonical_deptype(
            ('build', 'link')) == ('build', 'link')
        assert canonical_deptype(
            ('build', 'run')) == ('build', 'run')

        # lists
        assert canonical_deptype(
            ['build', 'link', 'run']) == ('build', 'link', 'run')
        assert canonical_deptype(
            ['build', 'link']) == ('build', 'link')
        assert canonical_deptype(
            ['build', 'run']) == ('build', 'run')

        # sorting
        assert canonical_deptype(
            ('run', 'build', 'link')) == ('build', 'link', 'run')
        assert canonical_deptype(
            ('run', 'link', 'build')) == ('build', 'link', 'run')
        assert canonical_deptype(
            ('run', 'link')) == ('link', 'run')
        assert canonical_deptype(
            ('link', 'build')) == ('build', 'link')

        # can't put 'all' in tuple or list
        with pytest.raises(ValueError):
            canonical_deptype(['all'])
        with pytest.raises(ValueError):
            canonical_deptype(('all',))

        # invalid values
        with pytest.raises(ValueError):
            canonical_deptype('foo')
        with pytest.raises(ValueError):
            canonical_deptype(('foo', 'bar'))
        with pytest.raises(ValueError):
            canonical_deptype(('foo',))

    def test_invalid_literal_spec(self):

        # Can't give type 'build' to a top-level spec
        with pytest.raises(spack.spec.SpecParseError):
            Spec.from_literal({'foo:build': None})

        # Can't use more than one ':' separator
        with pytest.raises(KeyError):
            Spec.from_literal({'foo': {'bar:build:link': None}})
