# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import archspec.cpu

import spack.config
import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
from spack.environment.environment import ViewDescriptor
from spack.version import Version

pytestmark = [pytest.mark.usefixtures("enable_runtimes")]


def _concretize_with_reuse(*, root_str, reused_str):
    reused_spec = spack.spec.Spec(reused_str).concretized()
    setup = spack.solver.asp.SpackSolverSetup(tests=False)
    driver = spack.solver.asp.PyclingoDriver()
    result, _, _ = driver.solve(setup, [spack.spec.Spec(f"{root_str}")], reuse=[reused_spec])
    root = result.specs[0]
    return root, reused_spec


@pytest.fixture
def runtime_repo(mutable_config):
    repo = os.path.join(spack.paths.repos_path, "compiler_runtime.test")
    with spack.repo.use_repositories(repo) as mock_repo:
        yield mock_repo


@pytest.fixture
def enable_runtimes():
    original = spack.solver.asp.WITH_RUNTIME
    spack.solver.asp.WITH_RUNTIME = True
    yield
    spack.solver.asp.WITH_RUNTIME = original


def test_correct_gcc_runtime_is_injected_as_dependency(runtime_repo):
    s = spack.spec.Spec("pkg-a%gcc@10.2.1 ^pkg-b%gcc@9.4.0").concretized()
    a, b = s["pkg-a"], s["pkg-b"]

    # Both a and b should depend on the same gcc-runtime directly
    assert a.dependencies("gcc-runtime") == b.dependencies("gcc-runtime")

    # And the gcc-runtime version should be that of the newest gcc used in the dag.
    assert a["gcc-runtime"].version == Version("10.2.1")


@pytest.mark.regression("41972")
def test_external_nodes_do_not_have_runtimes(runtime_repo, mutable_config, tmp_path):
    """Tests that external nodes don't have runtime dependencies."""

    packages_yaml = {"pkg-b": {"externals": [{"spec": "pkg-b@1.0", "prefix": f"{str(tmp_path)}"}]}}
    spack.config.set("packages", packages_yaml)

    s = spack.spec.Spec("pkg-a%gcc@10.2.1").concretized()

    a, b = s["pkg-a"], s["pkg-b"]

    # Since b is an external, it doesn't depend on gcc-runtime
    assert a.dependencies("gcc-runtime")
    assert a.dependencies("pkg-b")
    assert not b.dependencies("gcc-runtime")


@pytest.mark.parametrize(
    "root_str,reused_str,expected,nruntime",
    [
        # The reused runtime is older than we need, thus we'll add a more recent one for a
        (
            "pkg-a%gcc@10.2.1",
            "pkg-b%gcc@9.4.0",
            {"pkg-a": "gcc-runtime@10.2.1", "pkg-b": "gcc-runtime@9.4.0"},
            2,
        ),
        # The root is compiled with an older compiler, thus we'll NOT reuse the runtime from b
        (
            "pkg-a%gcc@9.4.0",
            "pkg-b%gcc@10.2.1",
            {"pkg-a": "gcc-runtime@9.4.0", "pkg-b": "gcc-runtime@9.4.0"},
            1,
        ),
        # Same as before, but tests that we can reuse from a more generic target
        pytest.param(
            "pkg-a%gcc@9.4.0",
            "pkg-b%gcc@10.2.1 target=x86_64",
            {"pkg-a": "gcc-runtime@9.4.0", "pkg-b": "gcc-runtime@9.4.0"},
            1,
            marks=pytest.mark.skipif(
                str(archspec.cpu.host().family) != "x86_64", reason="test data is x86_64 specific"
            ),
        ),
        pytest.param(
            "pkg-a%gcc@10.2.1",
            "pkg-b%gcc@9.4.0 target=x86_64",
            {
                "pkg-a": "gcc-runtime@10.2.1 target=x86_64",
                "pkg-b": "gcc-runtime@9.4.0 target=x86_64",
            },
            2,
            marks=pytest.mark.skipif(
                str(archspec.cpu.host().family) != "x86_64", reason="test data is x86_64 specific"
            ),
        ),
    ],
)
@pytest.mark.regression("44444")
def test_reusing_specs_with_gcc_runtime(root_str, reused_str, expected, nruntime, runtime_repo):
    """Tests that we can reuse specs with a "gcc-runtime" leaf node. In particular, checks
    that the semantic for gcc-runtimes versions accounts for reused packages too.

    Reusable runtime versions should be lower, or equal, to that of parent nodes.
    """
    root, reused_spec = _concretize_with_reuse(root_str=root_str, reused_str=reused_str)

    runtime_a = root.dependencies("gcc-runtime")[0]
    assert runtime_a.satisfies(expected["pkg-a"])
    runtime_b = root["pkg-b"].dependencies("gcc-runtime")[0]
    assert runtime_b.satisfies(expected["pkg-b"])

    runtimes = [x for x in root.traverse() if x.name == "gcc-runtime"]
    assert len(runtimes) == nruntime


@pytest.mark.parametrize(
    "root_str,reused_str,expected,not_expected",
    [
        # Ensure that, whether we have multiple runtimes in the DAG or not,
        # we always link only the latest version
        ("pkg-a%gcc@10.2.1", "pkg-b%gcc@9.4.0", ["gcc-runtime@10.2.1"], ["gcc-runtime@9.4.0"])
    ],
)
def test_views_can_handle_duplicate_runtime_nodes(
    root_str, reused_str, expected, not_expected, runtime_repo, tmp_path, monkeypatch
):
    """Tests that an environment is able to select the latest version of a runtime node to be
    linked in a view, in case more than one compatible version is in the DAG.
    """
    root, reused_spec = _concretize_with_reuse(root_str=root_str, reused_str=reused_str)

    # Mock the installation status to allow selecting nodes for the view
    monkeypatch.setattr(spack.spec.Spec, "installed", True)
    nodes = list(root.traverse())

    view = ViewDescriptor(str(tmp_path), str(tmp_path))
    candidate_specs = view.specs_for_view(nodes)

    for x in expected:
        assert any(node.satisfies(x) for node in candidate_specs)

    for x in not_expected:
        assert all(not node.satisfies(x) for node in candidate_specs)
