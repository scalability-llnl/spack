# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.config
import spack.environment as ev
import spack.package_base
import spack.traverse
from spack.cmd.stage import StageFilter
from spack.main import SpackCommand, SpackCommandError
from spack.spec import Spec
from spack.version import Version

stage = SpackCommand("stage")
env = SpackCommand("env")

pytestmark = pytest.mark.usefixtures("install_mockery", "mock_packages")


@pytest.mark.disable_clean_stage_check
def test_stage_spec(monkeypatch):
    """Verify that staging specs works."""

    expected = set(["trivial-install-test-package", "mpileaks"])

    def fake_stage(pkg, mirror_only=False):
        expected.remove(pkg.name)

    monkeypatch.setattr(spack.package_base.PackageBase, "do_stage", fake_stage)

    stage("trivial-install-test-package", "mpileaks")

    assert len(expected) == 0


@pytest.fixture(scope="function")
def check_stage_path(monkeypatch, tmpdir):
    expected_path = os.path.join(str(tmpdir), "x")

    def fake_stage(pkg, mirror_only=False):
        assert pkg.path == expected_path

    monkeypatch.setattr(spack.package_base.PackageBase, "do_stage", fake_stage)

    return expected_path


def test_stage_path(check_stage_path):
    """Verify that --path only works with single specs."""
    stage("--path={0}".format(check_stage_path), "trivial-install-test-package")


def test_stage_path_errors_multiple_specs(check_stage_path):
    """Verify that --path only works with single specs."""
    with pytest.raises(SpackCommandError):
        stage(f"--path={check_stage_path}", "trivial-install-test-package", "mpileaks")


@pytest.mark.disable_clean_stage_check
def test_stage_with_env_outside_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage concretizes specs not in environment instead of erroring."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.name == "trivial-install-test-package"
        assert pkg.path is None

    monkeypatch.setattr(spack.package_base.PackageBase, "do_stage", fake_stage)

    e = ev.create("test")
    e.add("mpileaks")
    e.concretize()

    with e:
        stage("trivial-install-test-package")


@pytest.mark.disable_clean_stage_check
def test_stage_with_env_inside_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage filters specs in environment instead of reconcretizing."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.name == "mpileaks"
        assert pkg.version == Version("100.100")

    monkeypatch.setattr(spack.package_base.PackageBase, "do_stage", fake_stage)

    e = ev.create("test")
    e.add("mpileaks@=100.100")
    e.concretize()

    with e:
        stage("mpileaks")


@pytest.mark.disable_clean_stage_check
def test_stage_full_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage filters specs in environment."""

    e = ev.create("test")
    e.add("mpileaks@=100.100")
    e.concretize()

    # list all the package names that should be staged
    expected = set(dep.name for dep in spack.traverse.traverse_nodes(e.concrete_roots()))

    # pop the package name from the list instead of actually staging
    def fake_stage(pkg, mirror_only=False):
        expected.remove(pkg.name)

    monkeypatch.setattr(spack.package_base.PackageBase, "do_stage", fake_stage)

    with e:
        stage()

    # assert that all were staged
    assert len(expected) == 0


@pytest.mark.disable_clean_stage_check
def test_concretizer_arguments(mock_packages, mock_fetch):
    """Make sure stage also has --reuse and --fresh flags."""
    stage("--reuse", "trivial-install-test-package")
    assert spack.config.get("concretizer:reuse", None) is True

    stage("--fresh", "trivial-install-test-package")
    assert spack.config.get("concretizer:reuse", None) is False


@pytest.mark.maybeslow
@pytest.mark.parametrize("externals", [["libelf"], []])
@pytest.mark.parametrize(
    "installed, skip_installed", [(["libdwarf"], False), (["libdwarf"], True)]
)
@pytest.mark.parametrize("exclusions", [["mpich", "callpath"], []])
def test_stage_spec_filters(
    mutable_mock_env_path,
    mock_packages,
    mock_fetch,
    externals,
    installed,
    skip_installed,
    exclusions,
    monkeypatch,
):
    e = ev.create("test")
    e.add("mpileaks@=100.100")
    e.concretize()
    all_specs = e.all_specs()

    def is_installed(self):
        return self.name in installed

    if skip_installed:
        monkeypatch.setattr(Spec, "installed", is_installed)

    should_be_filtered = []
    for spec in all_specs:
        for ext in externals:
            if spec.satisfies(Spec(ext)):
                spec.external_path = "/usr"
                assert spec.external
                should_be_filtered.append(spec)
        for ins in installed:
            if skip_installed and spec.satisfies(Spec(ins)):
                assert spec.installed
                should_be_filtered.append(spec)
        for exc in exclusions:
            if spec.satisfies(Spec(exc)):
                should_be_filtered.append(spec)

    filter = StageFilter(exclusions, skip_installed=skip_installed)
    specs_to_stage = [s for s in all_specs if not filter(s)]
    specs_were_filtered = [skip not in specs_to_stage for skip in should_be_filtered]

    assert all(
        specs_were_filtered
    ), f"Packages associated with bools: {[s.name for s in should_be_filtered]}"
