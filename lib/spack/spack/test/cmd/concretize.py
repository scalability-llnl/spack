# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import spack.environment as ev
from spack import spack_version
from spack.main import SpackCommand

pytestmark = pytest.mark.usefixtures("mutable_config", "mutable_mock_repo")

env = SpackCommand("env")
add = SpackCommand("add")
concretize = SpackCommand("concretize")


unification_strategies = [False, True, "when_possible"]


@pytest.mark.parametrize("unify", unification_strategies)
def test_concretize_all_test_dependencies(unify, mutable_mock_env_path):
    """Check all test dependencies are concretized."""
    env("create", "test")

    with ev.read("test") as e:
        e.unify = unify
        add("depb")
        concretize("--test", "all")
        assert e.matching_spec("test-dependency")


@pytest.mark.parametrize("unify", unification_strategies)
def test_concretize_root_test_dependencies_not_recursive(unify, mutable_mock_env_path):
    """Check that test dependencies are not concretized recursively."""
    env("create", "test")

    with ev.read("test") as e:
        e.unify = unify
        add("depb")
        concretize("--test", "root")
        assert e.matching_spec("test-dependency") is None


@pytest.mark.parametrize("unify", unification_strategies)
def test_concretize_root_test_dependencies_are_concretized(unify, mutable_mock_env_path):
    """Check that root test dependencies are concretized."""
    env("create", "test")

    with ev.read("test") as e:
        e.unify = unify
        add("pkg-a")
        add("pkg-b")
        concretize("--test", "root")
        assert e.matching_spec("test-dependency")

        data = e._to_lockfile_dict()
        assert data["spack"]["version"] == spack_version
