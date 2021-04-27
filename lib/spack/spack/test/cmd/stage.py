# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
from spack.main import SpackCommand
import spack.environment as ev
import spack.repo
from spack.version import Version


stage = SpackCommand('stage')
env = SpackCommand('env')

pytestmark = pytest.mark.usefixtures('install_mockery', 'mock_packages')


def test_stage_spec(monkeypatch):
    """Verify that staging specs works."""

    expected = set(['trivial-install-test-package', 'mpileaks'])

    def fake_stage(pkg, mirror_only=False):
        expected.remove(pkg.name)

    monkeypatch.setattr(spack.package.PackageBase, 'do_stage', fake_stage)

    stage('trivial-install-test-package', 'mpileaks')

    assert len(expected) == 0


def test_stage_path(monkeypatch):
    """Verify that --path only works with single specs."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.path == 'x'

    monkeypatch.setattr(spack.package.PackageBase, 'do_stage', fake_stage)

    stage('--path=x', 'trivial-install-test-package')


def test_stage_path_errors_multiple_specs(monkeypatch):
    """Verify that --path only works with single specs."""

    def fake_stage(pkg, mirror_only=False):
        pass

    monkeypatch.setattr(spack.package.PackageBase, 'do_stage', fake_stage)

    with pytest.raises(spack.main.SpackCommandError):
        stage('--path=x', 'trivial-install-test-package', 'mpileaks')


def test_stage_with_env_outside_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage concretizes specs not in environment instead of erroring."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.name == 'trivial-install-test-package'
        assert pkg.path is None

    monkeypatch.setattr(spack.package.PackageBase, 'do_stage', fake_stage)

    e = ev.create('test')
    e.add('mpileaks')
    e.concretize()

    with e:
        stage('trivial-install-test-package')


def test_stage_with_env_inside_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage filters specs in environment instead of reconcretizing."""

    def fake_stage(pkg, mirror_only=False):
        assert pkg.name == 'mpileaks'
        assert pkg.version == Version('100.100')

    monkeypatch.setattr(spack.package.PackageBase, 'do_stage', fake_stage)

    e = ev.create('test')
    e.add('mpileaks@100.100')
    e.concretize()

    with e:
        stage('mpileaks')


def test_stage_full_env(mutable_mock_env_path, monkeypatch):
    """Verify that stage filters specs in environment."""

    e = ev.create('test')
    e.add('mpileaks@100.100')
    e.concretize()

    # list all the package names that should be staged
    expected = set()
    for spec in e.specs_by_hash.values():
        for dep in spec.traverse():
            expected.add(dep.name)

    # pop the package name from the list instead of actually staging
    def fake_stage(pkg, mirror_only=False):
        expected.remove(pkg.name)

    monkeypatch.setattr(spack.package.PackageBase, 'do_stage', fake_stage)

    with e:
        stage()

    # assert that all were staged
    assert len(expected) == 0
