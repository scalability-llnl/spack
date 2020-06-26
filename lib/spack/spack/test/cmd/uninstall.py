# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import llnl.util.tty as tty
import spack.store
from spack.main import SpackCommand, SpackCommandError

uninstall = SpackCommand('uninstall')
install = SpackCommand('install')


class MockArgs(object):

    def __init__(self, packages, all=False, force=False, dependents=False):
        self.packages = packages
        self.all = all
        self.force = force
        self.dependents = dependents
        self.yes_to_all = True


@pytest.mark.db
def test_multiple_matches(mutable_database):
    """Test unable to uninstall when multiple matches."""
    with pytest.raises(SpackCommandError):
        uninstall('-y', 'mpileaks')


@pytest.mark.db
def test_installed_dependents(mutable_database):
    """Test can't uninstall when there are installed dependents."""
    with pytest.raises(SpackCommandError):
        uninstall('-y', 'libelf')


@pytest.mark.db
def test_recursive_uninstall(mutable_database):
    """Test recursive uninstall."""
    uninstall('-y', '-a', '--dependents', 'callpath')

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 8
    # query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
    callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
    mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

    assert len(mpileaks_specs) == 0
    assert len(callpath_specs) == 0
    assert len(mpi_specs) == 3


@pytest.mark.db
@pytest.mark.regression('3690')
@pytest.mark.parametrize('constraint,expected_number_of_specs', [
    ('dyninst', 7), ('libelf', 5)
])
def test_uninstall_spec_with_multiple_roots(
        constraint, expected_number_of_specs, mutable_database
):
    uninstall('-y', '-a', '--dependents', constraint)

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == expected_number_of_specs


@pytest.mark.db
@pytest.mark.parametrize('constraint,expected_number_of_specs', [
    ('dyninst', 13), ('libelf', 13)
])
def test_force_uninstall_spec_with_ref_count_not_zero(
        constraint, expected_number_of_specs, mutable_database
):
    uninstall('-f', '-y', constraint)

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == expected_number_of_specs


@pytest.mark.db
@pytest.mark.usefixtures('mutable_database')
def test_global_recursive_uninstall():
    """Test recursive uninstall from global upstream"""
    uninstall('-g', '-y', '-a', '--dependents', 'callpath')

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 8
    # query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
    callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
    mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

    assert len(mpileaks_specs) == 0
    assert len(callpath_specs) == 0
    assert len(mpi_specs) == 3


@pytest.mark.db
@pytest.mark.usefixtures('mutable_database')
def test_upstream_recursive_uninstall():
    """Test recursive uninstall from specified upstream"""
    uninstall('--upstream=global', '-y', '-a', '--dependents', 'callpath')

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 8
    # query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
    callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
    mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

    assert len(mpileaks_specs) == 0
    assert len(callpath_specs) == 0
    assert len(mpi_specs) == 3


def test_force_uninstall_and_reinstall_by_hash(mutable_database):
    """Test forced uninstall and reinstall of old specs."""
    # this is the spec to be removed
    callpath_spec = spack.store.db.query_one('callpath ^mpich')
    dag_hash = callpath_spec.dag_hash()

    # ensure can look up by hash and that it's a dependent of mpileaks
    def validate_callpath_spec(installed):
        assert installed is True or installed is False

        specs = spack.store.db.get_by_hash(dag_hash, installed=installed)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.db.get_by_hash(dag_hash[:7], installed=installed)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.db.get_by_hash(dag_hash, installed=any)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.db.get_by_hash(dag_hash[:7], installed=any)
        assert len(specs) == 1 and specs[0] == callpath_spec

        # specs = spack.store.db.get_by_hash(dag_hash, installed=not installed)
        # assert specs is None

        # specs = spack.store.db.get_by_hash(dag_hash[:7],
        #                                    installed=not installed)
        # assert specs is None

        mpileaks_spec = spack.store.db.query_one('mpileaks ^mpich')
        assert callpath_spec in mpileaks_spec

        spec = spack.store.db.query_one('callpath ^mpich', installed=installed)
        assert spec == callpath_spec

        spec = spack.store.db.query_one('callpath ^mpich', installed=any)
        assert spec == callpath_spec

        spec = spack.store.db.query_one('callpath ^mpich',
                                        installed=not installed)
        assert spec is None

    validate_callpath_spec(True)

    uninstall('-y', '-f', 'callpath ^mpich')

    # ensure that you can still look up by hash and see deps, EVEN though
    # the callpath spec is missing.
    validate_callpath_spec(False)

    # BUT, make sure that the removed callpath spec is not in queries
    def db_specs():
        all_specs = spack.store.layout.all_specs()
        return (
            all_specs,
            [s for s in all_specs if s.satisfies('mpileaks')],
            [s for s in all_specs if s.satisfies('callpath')],
            [s for s in all_specs if s.satisfies('mpi')]
        )
    all_specs, mpileaks_specs, callpath_specs, mpi_specs = db_specs()
    assert len(all_specs) == 13
    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 2
    assert len(mpi_specs) == 3

    # Now, REINSTALL the spec and make sure everything still holds
    install('--fake', '/%s' % dag_hash[:7])

    validate_callpath_spec(True)

    all_specs, mpileaks_specs, callpath_specs, mpi_specs = db_specs()
    assert len(all_specs) == 14      # back to 14
    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3  # back to 3
    assert len(mpi_specs) == 3


@pytest.mark.db
@pytest.mark.regression('15773')
def test_in_memory_consistency_when_uninstalling(
        mutable_database, monkeypatch
):
    """Test that uninstalling doesn't raise warnings"""
    def _warn(*args, **kwargs):
        raise RuntimeError('a warning was triggered!')
    monkeypatch.setattr(tty, 'warn', _warn)
    # Now try to uninstall and check this doesn't trigger warnings
    uninstall('-y', '-a')
