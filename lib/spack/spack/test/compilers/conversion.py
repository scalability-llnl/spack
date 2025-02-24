# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests conversions from compilers.yaml"""
import pytest

from spack.compilers.config import CompilerFactory


@pytest.fixture()
def mock_compiler(mock_executable):
    gcc = mock_executable("gcc", "echo 13.2.0")
    gxx = mock_executable("g++", "echo 13.2.0")
    gfortran = mock_executable("gfortran", "echo 13.2.0")
    return {
        "spec": "gcc@13.2.0",
        "paths": {"cc": str(gcc), "cxx": str(gxx), "f77": str(gfortran), "fc": str(gfortran)},
    }


# - compiler:
#     spec: clang@=10.0.0
#     paths:
#       cc: /usr/bin/clang
#       cxx: /usr/bin/clang++
#       f77: null
#       fc: null
#     flags: {}
#     operating_system: ubuntu20.04
#     target: x86_64
#     modules: []
#     environment: {}
#     extra_rpaths: []


def test_basic_compiler_conversion(mock_compiler, tmp_path):
    """Tests the conversion of a compiler using a single toolchain, with default options."""
    compilers = CompilerFactory.from_legacy_yaml(mock_compiler)
    compiler_spec = compilers[0]
    assert compiler_spec.satisfies("gcc@13.2.0 languages=c,c++,fortran")
    assert compiler_spec.external
    assert compiler_spec.external_path == str(tmp_path)

    for language in ("c", "cxx", "fortran"):
        assert language in compiler_spec.extra_attributes["compilers"]


def test_compiler_conversion_with_flags(mock_compiler):
    """Tests that flags are converted appropriately for external compilers"""
    mock_compiler["flags"] = {"cflags": "-O3", "cxxflags": "-O2 -g"}
    compiler_spec = CompilerFactory.from_legacy_yaml(mock_compiler)[0]
    assert compiler_spec.external
    assert "flags" in compiler_spec.extra_attributes
    assert compiler_spec.extra_attributes["flags"]["cflags"] == "-O3"
    assert compiler_spec.extra_attributes["flags"]["cxxflags"] == "-O2 -g"


def tests_compiler_conversion_with_environment(mock_compiler):
    """Tests that custom environment modifications are converted appropriately
    for external compilers
    """
    mods = {"set": {"FOO": "foo", "BAR": "bar"}, "unset": ["BAZ"]}
    mock_compiler["environment"] = mods
    compiler_spec = CompilerFactory.from_legacy_yaml(mock_compiler)[0]
    assert compiler_spec.external
    assert "environment" in compiler_spec.extra_attributes
    assert compiler_spec.extra_attributes["environment"] == mods


def tests_compiler_conversion_extra_rpaths(mock_compiler):
    """Tests that extra rpaths are converted appropriately for external compilers"""
    mock_compiler["extra_rpaths"] = ["/foo/bar"]
    compiler_spec = CompilerFactory.from_legacy_yaml(mock_compiler)[0]
    assert compiler_spec.external
    assert "extra_rpaths" in compiler_spec.extra_attributes
    assert compiler_spec.extra_attributes["extra_rpaths"] == ["/foo/bar"]


def tests_compiler_conversion_modules(mock_compiler):
    """Tests that modules are converted appropriately for external compilers"""
    modules = ["foo/4.1.2", "bar/5.1.4"]
    mock_compiler["modules"] = modules
    compiler_spec = CompilerFactory.from_legacy_yaml(mock_compiler)[0]
    assert compiler_spec.external
    assert compiler_spec.external_modules == modules
