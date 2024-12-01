# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.error
import spack.installer as inst
import spack.repo
import spack.spec


def test_build_task_errors(install_mockery):
    """Check expected errors when instantiating a BuildTask."""
    spec = spack.spec.Spec("trivial-install-test-package")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)

    # The value of the request argument is expected to not be checked.
    for pkg in [None, "abc"]:
        with pytest.raises(TypeError, match="must be a package"):
            inst.BuildTask(pkg, None)

    with pytest.raises(ValueError, match="must have a concrete spec"):
        inst.BuildTask(pkg_cls(spec), None)

    # Using a concretized package now means the request argument is checked.
    spec.concretize()
    assert spec.concrete

    with pytest.raises(TypeError, match="is not a valid build request"):
        inst.BuildTask(spec.package, None)

    # Using a valid package and spec, the next check is the status argument.
    request = inst.BuildRequest(spec.package, {})

    with pytest.raises(TypeError, match="is not a valid build status"):
        inst.BuildTask(spec.package, request, status="queued")

    # Now we can check that build tasks cannot be create when the status
    # indicates the task is/should've been removed.
    with pytest.raises(spack.error.InstallError, match="Cannot create a task"):
        inst.BuildTask(spec.package, request, status=inst.BuildStatus.REMOVED)

    # Also make sure to not accept an incompatible installed argument value.
    with pytest.raises(TypeError, match="'installed' be a 'set', not 'str'"):
        inst.BuildTask(spec.package, request, installed="mpileaks")


def test_build_task_basics(install_mockery):
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    task = inst.BuildTask(spec.package, request=request, status=inst.BuildStatus.QUEUED)
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
    task = inst.BuildTask(spec.package, request=request, status=inst.BuildStatus.QUEUED)

    # Cover __repr__
    irep = task.__repr__()
    assert irep.startswith(task.__class__.__name__)
    assert "BuildStatus.QUEUED" in irep
    assert "sequence=" in irep

    # Cover __str__
    istr = str(task)
    assert "status=queued" in istr  # == BuildStatus.QUEUED
    assert "#dependencies=1" in istr
    assert "priority=" in istr
