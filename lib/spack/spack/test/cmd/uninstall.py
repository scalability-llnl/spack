# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import llnl.util.tty as tty

import spack.cmd.uninstall
import spack.environment
import spack.store
from spack.main import SpackCommand, SpackCommandError

uninstall = SpackCommand("uninstall")
install = SpackCommand("install")


class MockArgs:
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
        uninstall("-y", "mpileaks")


@pytest.mark.db
def test_installed_dependents(mutable_database):
    """Test can't uninstall when there are installed dependents."""
    with pytest.raises(SpackCommandError):
        uninstall("-y", "libelf")


@pytest.mark.db
def test_correct_installed_dependents(mutable_database):
    # Test whether we return the right dependents.

    # Take callpath from the database
    callpath = spack.store.STORE.db.query_local("callpath")[0]

    # Ensure it still has dependents and dependencies
    dependents = callpath.dependents(deptype=("run", "link"))
    dependencies = callpath.dependencies(deptype=("run", "link"))
    assert dependents and dependencies

    # Uninstall it, so it's missing.
    callpath.package.do_uninstall(force=True)

    # Retrieve all dependent hashes
    dependents = spack.cmd.uninstall.installed_dependents(dependencies)
    assert dependents

    dependent_hashes = [s.dag_hash() for s in dependents]
    set_dependent_hashes = set(dependent_hashes)

    # Assert uniqueness
    assert len(dependent_hashes) == len(set_dependent_hashes)

    # Ensure parents of callpath are listed
    assert all(s.dag_hash() in set_dependent_hashes for s in dependents)

    # Ensure callpath itself is not, since it was missing.
    assert callpath.dag_hash() not in set_dependent_hashes


@pytest.mark.db
def test_recursive_uninstall(mutable_database):
    """Test recursive uninstall."""
    uninstall("-y", "-a", "--dependents", "callpath")

    all_specs = spack.store.STORE.layout.all_specs()
    assert len(all_specs) == 9
    # query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies("mpileaks")]
    callpath_specs = [s for s in all_specs if s.satisfies("callpath")]
    mpi_specs = [s for s in all_specs if s.satisfies("mpi")]

    assert len(mpileaks_specs) == 0
    assert len(callpath_specs) == 0
    assert len(mpi_specs) == 3


@pytest.mark.db
@pytest.mark.regression("3690")
@pytest.mark.parametrize("constraint,expected_number_of_specs", [("dyninst", 8), ("libelf", 6)])
def test_uninstall_spec_with_multiple_roots(
    constraint, expected_number_of_specs, mutable_database
):
    uninstall("-y", "-a", "--dependents", constraint)

    all_specs = spack.store.STORE.layout.all_specs()
    assert len(all_specs) == expected_number_of_specs


@pytest.mark.db
@pytest.mark.parametrize("constraint,expected_number_of_specs", [("dyninst", 14), ("libelf", 14)])
def test_force_uninstall_spec_with_ref_count_not_zero(
    constraint, expected_number_of_specs, mutable_database
):
    uninstall("-f", "-y", constraint)

    all_specs = spack.store.STORE.layout.all_specs()
    assert len(all_specs) == expected_number_of_specs


@pytest.mark.db
def test_force_uninstall_and_reinstall_by_hash(mutable_database):
    """Test forced uninstall and reinstall of old specs."""
    # this is the spec to be removed
    callpath_spec = spack.store.STORE.db.query_one("callpath ^mpich")
    dag_hash = callpath_spec.dag_hash()

    # ensure can look up by hash and that it's a dependent of mpileaks
    def validate_callpath_spec(installed):
        assert installed is True or installed is False

        specs = spack.store.STORE.db.get_by_hash(dag_hash, installed=installed)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.STORE.db.get_by_hash(dag_hash[:7], installed=installed)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.STORE.db.get_by_hash(dag_hash, installed=any)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.STORE.db.get_by_hash(dag_hash[:7], installed=any)
        assert len(specs) == 1 and specs[0] == callpath_spec

        specs = spack.store.STORE.db.get_by_hash(dag_hash, installed=not installed)
        assert specs is None

        specs = spack.store.STORE.db.get_by_hash(dag_hash[:7], installed=not installed)
        assert specs is None

        mpileaks_spec = spack.store.STORE.db.query_one("mpileaks ^mpich")
        assert callpath_spec in mpileaks_spec

        spec = spack.store.STORE.db.query_one("callpath ^mpich", installed=installed)
        assert spec == callpath_spec

        spec = spack.store.STORE.db.query_one("callpath ^mpich", installed=any)
        assert spec == callpath_spec

        spec = spack.store.STORE.db.query_one("callpath ^mpich", installed=not installed)
        assert spec is None

    validate_callpath_spec(True)

    uninstall("-y", "-f", "callpath ^mpich")

    # ensure that you can still look up by hash and see deps, EVEN though
    # the callpath spec is missing.
    validate_callpath_spec(False)

    # BUT, make sure that the removed callpath spec is not in queries
    def db_specs():
        all_specs = spack.store.STORE.layout.all_specs()
        return (
            all_specs,
            [s for s in all_specs if s.satisfies("mpileaks")],
            [s for s in all_specs if s.satisfies("callpath")],
            [s for s in all_specs if s.satisfies("mpi")],
        )

    all_specs, mpileaks_specs, callpath_specs, mpi_specs = db_specs()
    total_specs = len(all_specs)
    assert total_specs == 14
    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 2
    assert len(mpi_specs) == 3

    # Now, REINSTALL the spec and make sure everything still holds
    install("--fake", "/%s" % dag_hash[:7])

    validate_callpath_spec(True)

    all_specs, mpileaks_specs, callpath_specs, mpi_specs = db_specs()
    assert len(all_specs) == total_specs + 1  # back to total_specs+1
    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3  # back to 3
    assert len(mpi_specs) == 3


@pytest.mark.db
@pytest.mark.regression("15773")
def test_in_memory_consistency_when_uninstalling(mutable_database, monkeypatch):
    """Test that uninstalling doesn't raise warnings"""

    def _warn(*args, **kwargs):
        raise RuntimeError("a warning was triggered!")

    monkeypatch.setattr(tty, "warn", _warn)
    # Now try to uninstall and check this doesn't trigger warnings
    uninstall("-y", "-a")


# Note: I want to use https://docs.pytest.org/en/7.1.x/how-to/skipping.html#skip-all-test-functions-of-a-class-or-module
# the style formatter insists on separating these two lines.
class TestUninstallFromEnv:
    """Tests an installation with two environments e1 and e2, which each have
    shared package installations:

    e1 has diamond-link-left -> diamond-link-bottom

    e2 has diamond-link-right -> diamond-link-bottom
    """

    env = SpackCommand("env")
    add = SpackCommand("add")
    concretize = SpackCommand("concretize")
    find = SpackCommand("find")

    @pytest.fixture(scope="function")
    def environment_setup(
        self, mutable_mock_env_path, mock_packages, mutable_database, install_mockery
    ):
        TestUninstallFromEnv.env("create", "e1")
        e1 = spack.environment.read("e1")
        with e1:
            TestUninstallFromEnv.add("diamond-link-left")
            TestUninstallFromEnv.add("diamond-link-bottom")
            TestUninstallFromEnv.concretize()
            install("--fake")

        TestUninstallFromEnv.env("create", "e2")
        e2 = spack.environment.read("e2")
        with e2:
            TestUninstallFromEnv.add("diamond-link-right")
            TestUninstallFromEnv.add("diamond-link-bottom")
            TestUninstallFromEnv.concretize()
            install("--fake")
        yield "environment_setup"
        TestUninstallFromEnv.env("rm", "e1", "-y")
        TestUninstallFromEnv.env("rm", "e2", "-y")

    def test_basic_env_sanity(self, environment_setup):
        for env_name in ["e1", "e2"]:
            e = spack.environment.read(env_name)
            with e:
                for _, concretized_spec in e.concretized_specs():
                    assert concretized_spec.package.installed

    def test_uninstall_force_dependency_shared_between_envs(self, environment_setup):
        """If you "spack uninstall -f --dependents diamond-link-bottom" from
        e1, then all packages should be uninstalled (but not removed) from
        both e1 and e2.
        """
        e1 = spack.environment.read("e1")
        with e1:
            uninstall("-f", "-y", "--dependents", "diamond-link-bottom")

            # The specs should still be in the environment, since
            # --remove was not specified
            assert set(root.name for (root, _) in e1.concretized_specs()) == set(
                ["diamond-link-left", "diamond-link-bottom"]
            )

            for _, concretized_spec in e1.concretized_specs():
                assert not concretized_spec.package.installed

        # Everything in e2 depended on diamond-link-bottom, so should also
        # have been uninstalled. The roots should be unchanged though.
        e2 = spack.environment.read("e2")
        with e2:
            assert set(root.name for (root, _) in e2.concretized_specs()) == set(
                ["diamond-link-right", "diamond-link-bottom"]
            )
            for _, concretized_spec in e2.concretized_specs():
                assert not concretized_spec.package.installed

    def test_uninstall_remove_dependency_shared_between_envs(self, environment_setup):
        """If you "spack uninstall --dependents --remove diamond-link-bottom" from
        e1, then all packages are removed from e1 (it is now empty);
        diamond-link-left is also uninstalled (since only e1 needs it) but
        diamond-link-bottom is not uninstalled (since e2 needs it).
        """
        e1 = spack.environment.read("e1")
        with e1:
            dtdiamondleft = next(
                concrete
                for (_, concrete) in e1.concretized_specs()
                if concrete.name == "diamond-link-left"
            )
            output = uninstall("-y", "--dependents", "--remove", "diamond-link-bottom")
            assert "The following specs will be removed but not uninstalled" in output
            assert not list(e1.roots())
            assert not dtdiamondleft.package.installed

        # Since -f was not specified, all specs in e2 should still be installed
        # (and e2 should be unchanged)
        e2 = spack.environment.read("e2")
        with e2:
            assert set(root.name for (root, _) in e2.concretized_specs()) == set(
                ["diamond-link-right", "diamond-link-bottom"]
            )
            for _, concretized_spec in e2.concretized_specs():
                assert concretized_spec.package.installed

    def test_uninstall_dependency_shared_between_envs_fail(self, environment_setup):
        """If you "spack uninstall --dependents diamond-link-bottom" from
        e1 (without --remove or -f), then this should fail (this is needed by
        e2).
        """
        e1 = spack.environment.read("e1")
        with e1:
            output = uninstall("-y", "--dependents", "diamond-link-bottom", fail_on_error=False)
            assert "There are still dependents." in output
            assert "use `spack env remove`" in output

        # The environment should be unchanged and nothing should have been
        # uninstalled
        assert set(root.name for (root, _) in e1.concretized_specs()) == set(
            ["diamond-link-left", "diamond-link-bottom"]
        )
        for _, concretized_spec in e1.concretized_specs():
            assert concretized_spec.package.installed

    def test_uninstall_force_and_remove_dependency_shared_between_envs(self, environment_setup):
        """If you "spack uninstall -f --dependents --remove diamond-link-bottom" from
        e1, then all packages should be uninstalled and removed from e1.
        All packages will also be uninstalled from e2, but the roots will
        remain unchanged.
        """
        e1 = spack.environment.read("e1")
        with e1:
            dtdiamondleft = next(
                concrete
                for (_, concrete) in e1.concretized_specs()
                if concrete.name == "diamond-link-left"
            )
            uninstall("-f", "-y", "--dependents", "--remove", "diamond-link-bottom")
            assert not list(e1.roots())
            assert not dtdiamondleft.package.installed

        e2 = spack.environment.read("e2")
        with e2:
            assert set(root.name for (root, _) in e2.concretized_specs()) == set(
                ["diamond-link-right", "diamond-link-bottom"]
            )
            for _, concretized_spec in e2.concretized_specs():
                assert not concretized_spec.package.installed

    def test_uninstall_keep_dependents_dependency_shared_between_envs(self, environment_setup):
        """If you "spack uninstall -f --remove diamond-link-bottom" from
        e1, then diamond-link-bottom should be uninstalled, which leaves
        "dangling" references in both environments, since
        diamond-link-left and diamond-link-right both need it.
        """
        e1 = spack.environment.read("e1")
        with e1:
            dtdiamondleft = next(
                concrete
                for (_, concrete) in e1.concretized_specs()
                if concrete.name == "diamond-link-left"
            )
            uninstall("-f", "-y", "--remove", "diamond-link-bottom")
            # diamond-link-bottom was removed from the list of roots (note that
            # it would still be installed since diamond-link-left depends on it)
            assert set(x.name for x in e1.roots()) == set(["diamond-link-left"])
            assert dtdiamondleft.package.installed

        e2 = spack.environment.read("e2")
        with e2:
            assert set(root.name for (root, _) in e2.concretized_specs()) == set(
                ["diamond-link-right", "diamond-link-bottom"]
            )
            dtdiamondright = next(
                concrete
                for (_, concrete) in e2.concretized_specs()
                if concrete.name == "diamond-link-right"
            )
            assert dtdiamondright.package.installed
            dtdiamondbottom = next(
                concrete
                for (_, concrete) in e2.concretized_specs()
                if concrete.name == "diamond-link-bottom"
            )
            assert not dtdiamondbottom.package.installed
