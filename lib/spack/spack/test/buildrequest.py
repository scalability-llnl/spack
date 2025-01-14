# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.deptypes as dt
import spack.installer as inst
import spack.repo
import spack.spec


def test_build_request_errors(install_mockery):
    with pytest.raises(ValueError, match="must be a package"):
        inst.BuildRequest("abc", {})

    spec = spack.spec.Spec("trivial-install-test-package")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    with pytest.raises(ValueError, match="must have a concrete spec"):
        inst.BuildRequest(pkg_cls(spec), {})


def test_build_request_basics(install_mockery):
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    assert not request.pkg.stop_before_phase
    assert not request.pkg.last_phase
    assert request.spec == spec.package.spec

    # Ensure key default install arguments are set
    assert "install_package" in request.install_args
    assert "install_deps" in request.install_args


def test_build_request_strings(install_mockery):
    """Tests of BuildRequest repr and str for coverage purposes."""
    # Using a package with one dependency
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})

    # Cover __repr__
    irep = request.__repr__()
    assert irep.startswith(request.__class__.__name__)

    # Cover __str__
    istr = str(request)
    assert "package=dependent-install" in istr
    assert "install_args=" in istr


@pytest.mark.parametrize(
    "include_build_deps,deptypes", [(True, dt.BUILD | dt.LINK | dt.RUN), (False, dt.LINK | dt.RUN)]
)
def test_build_request_deptypes(install_mockery, include_build_deps, deptypes):
    s = spack.spec.Spec("dependent-install").concretized()

    build_request = inst.BuildRequest(s.package, {"include_build_deps": include_build_deps})

    package_deptypes = build_request.get_depflags(s.package)
    dependency_deptypes = build_request.get_depflags(s["dependency-install"].package)

    assert package_deptypes == dependency_deptypes == deptypes
