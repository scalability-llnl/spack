# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test class methods on Package objects.

This doesn't include methods on package *instances* (like do_install(),
etc.).  Only methods like ``possible_dependencies()`` that deal with the
static DSL metadata for packages.
"""

import pytest
import spack.package
import spack.repo


@pytest.fixture(scope="module")
def mpi_names(mock_repo_path):
    return [spec.name for spec in mock_repo_path.providers_for('mpi')]


@pytest.fixture()
def mpileaks_possible_deps(mock_packages, mpi_names):
    possible = {
        'callpath': set(['dyninst'] + mpi_names),
        'dyninst': set(['libdwarf', 'libelf']),
        'fake': set(),
        'intel-parallel-studio': set(),
        'libdwarf': set(['libelf']),
        'libelf': set(),
        'mpich': set(),
        'mpich2': set(),
        'mpileaks': set(['callpath'] + mpi_names),
        'multi-provider-mpi': set(),
        'zmpi': set(['fake']),
    }
    return possible


def test_possible_dependencies(mock_packages, mpileaks_possible_deps):
    mpileaks = spack.repo.get('mpileaks')
    result = mpileaks.possible_dependencies(expand_virtuals=True)
    assert mpileaks_possible_deps == result

    assert {
        'callpath': set(['dyninst', 'mpi']),
        'dyninst': set(['libdwarf', 'libelf']),
        'libdwarf': set(['libelf']),
        'libelf': set(),
        'mpi': set(),
        'mpileaks': set(['callpath', 'mpi']),
    } == mpileaks.possible_dependencies(expand_virtuals=False)


def test_possible_direct_dependencies(mock_packages, mpileaks_possible_deps):
    mpileaks = spack.repo.get('mpileaks')
    deps = mpileaks.possible_dependencies(transitive=False,
                                          expand_virtuals=False)

    assert {
        'callpath': set(),
        'mpi': set(),
        'mpileaks': set(['callpath', 'mpi']),
    } == deps


def test_possible_dependencies_virtual(mock_packages, mpi_names):
    expected = dict(
        (name, set(spack.repo.get(name).dependencies))
        for name in mpi_names
    )

    # only one mock MPI has a dependency
    expected['fake'] = set()

    assert expected == spack.package.possible_dependencies(
        "mpi", transitive=False)


def test_possible_dependencies_missing(mock_packages):
    md = spack.repo.get("missing-dependency")
    missing = {}
    md.possible_dependencies(transitive=True, missing=missing)
    assert set([
        "this-is-a-missing-dependency"
    ]) == missing["missing-dependency"]


def test_possible_dependencies_with_deptypes(mock_packages):
    dtbuild1 = spack.repo.get('dtbuild1')

    assert {
        'dtbuild1': set(['dtrun2', 'dtlink2']),
        'dtlink2': set(),
        'dtrun2': set(),
    } == dtbuild1.possible_dependencies(deptype=('link', 'run'))

    assert {
        'dtbuild1': set(['dtbuild2', 'dtlink2']),
        'dtbuild2': set(),
        'dtlink2': set(),
    } == dtbuild1.possible_dependencies(deptype=('build'))

    assert {
        'dtbuild1': set(['dtlink2']),
        'dtlink2': set(),
    } == dtbuild1.possible_dependencies(deptype=('link'))


def test_possible_dependencies_with_multiple_classes(
        mock_packages, mpileaks_possible_deps):
    pkgs = ['dt-diamond', 'mpileaks']
    expected = mpileaks_possible_deps.copy()
    expected.update({
        'dt-diamond': set(['dt-diamond-left', 'dt-diamond-right']),
        'dt-diamond-left': set(['dt-diamond-bottom']),
        'dt-diamond-right': set(['dt-diamond-bottom']),
        'dt-diamond-bottom': set(),
    })

    assert expected == spack.package.possible_dependencies(*pkgs)
