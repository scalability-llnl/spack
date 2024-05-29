# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.installer as inst
import spack.repo
import spack.spec


def test_build_task_errors(install_mockery):
    with pytest.raises(ValueError, match="must be a package"):
        inst.BuildTask("abc", None, False, 0, 0, 0, set())

    spec = spack.spec.Spec("trivial-install-test-package")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    with pytest.raises(ValueError, match="must have a concrete spec"):
        inst.BuildTask(pkg_cls(spec), None, False, 0, 0, 0, set())

    spec.concretize()
    assert spec.concrete
    with pytest.raises(ValueError, match="must have a build request"):
        inst.BuildTask(spec.package, None, False, 0, 0, 0, set())

    request = inst.BuildRequest(spec.package, {})
    with pytest.raises(inst.InstallError, match="Cannot create a build task"):
        inst.BuildTask(spec.package, request, False, 0, 0, inst.STATUS_REMOVED, set())


def test_build_task_basics(install_mockery):
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    task = inst.BuildTask(spec.package, request, False, 0, 0, inst.STATUS_ADDED, set())
    assert not task.explicit
    assert task.priority == len(task.uninstalled_deps)
    assert task.key == (task.priority, task.sequence)

    # Ensure flagging installed works as expected
    assert len(task.uninstalled_deps) > 0
    assert task.dependencies == task.uninstalled_deps
    task.flag_installed(task.dependencies)
    assert len(task.uninstalled_deps) == 0
    assert task.priority == 0


def test_build_task_strings(install_mockery):
    """Tests of build_task repr and str for coverage purposes."""
    # Using a package with one dependency
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    task = inst.BuildTask(spec.package, request, False, 0, 0, inst.STATUS_ADDED, set())

    # Cover __repr__
    irep = task.__repr__()
    assert irep.startswith(task.__class__.__name__)
    assert "status='queued'" in irep  # == STATUS_ADDED
    assert "sequence=" in irep

    # Cover __str__
    istr = str(task)
    assert "status=queued" in istr  # == STATUS_ADDED
    assert "#dependencies=1" in istr
    assert "priority=" in istr
