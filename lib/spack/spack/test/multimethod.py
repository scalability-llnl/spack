# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test for multi_method dispatch."""

import pytest

import spack.config
import spack.platforms
import spack.spec
from spack.multimethod import NoSuchMethodError

pytestmark = [
    pytest.mark.usefixtures("mock_packages", "config"),
    pytest.mark.not_on_windows("Not running on windows"),
]


@pytest.fixture(scope="module", params=["multimethod", "multimethod-inheritor"])
def pkg_name(request):
    """Make tests run on both multimethod and multimethod-inheritor.

    This means we test all of our @when methods on a class that uses them
    directly, AND on a class that inherits them.
    """
    return request.param


def test_no_version_match(pkg_name):
    spec = spack.spec.Spec(pkg_name + "@2.0").concretized()
    with pytest.raises(NoSuchMethodError):
        spec.package.no_version_2()


@pytest.mark.parametrize(
    "constraint_str,method_name,expected_result",
    [
        # Only one version match these constraints
        ("@1.0", "no_version_2", 1),
        ("@3.0", "no_version_2", 3),
        ("@4.0", "no_version_2", 4),
        # These constraints overlap, in which case the first match wins
        ("@2.0", "version_overlap", 1),
        ("@5.0", "version_overlap", 2),
        # These constraints are on the version of a virtual dependency
        ("^mpich@3.0.4", "mpi_version", 3),
        ("^mpich2@1.2", "mpi_version", 2),
        ("^mpich@1.0", "mpi_version", 1),
        # Undefined mpi versions
        ("^mpich@=0.4", "mpi_version", 1),
        ("^mpich@=1.4", "mpi_version", 1),
        # Constraints on compilers with a default
        ("%gcc", "has_a_default", "gcc"),
        ("%clang", "has_a_default", "clang"),
        ("%apple-clang os=elcapitan", "has_a_default", "default"),
        # Constraints on dependencies
        ("^zmpi", "different_by_dep", "zmpi"),
        ("^mpich", "different_by_dep", "mpich"),
        # Constraints on virtual dependencies
        ("^mpich2", "different_by_virtual_dep", 2),
        ("^mpich@1.0", "different_by_virtual_dep", 1),
        # Multimethod with base classes
        ("@1", "base_method", "base_method"),
        # Boolean
        ("", "boolean_true_first", "True"),
        ("", "boolean_false_first", "True"),
    ],
)
def test_multimethod_calls(
    pkg_name, constraint_str, method_name, expected_result, compiler_factory
):
    # Add apple-clang, as it is required by one of the tests
    with spack.config.override(
        "compilers", [compiler_factory(spec="apple-clang@9.1.0", operating_system="elcapitan")]
    ):
        s = spack.spec.Spec(pkg_name + constraint_str).concretized()
    msg = f"Method {method_name} from {s} is giving a wrong result"
    assert getattr(s.package, method_name)() == expected_result, msg


def test_target_match(pkg_name):
    platform = spack.platforms.host()
    targets = list(platform.targets.values())
    for target in targets[:-1]:
        s = spack.spec.Spec(pkg_name + " target=" + target.name).concretized()
        assert s.package.different_by_target() == target.name

    s = spack.spec.Spec(pkg_name + " target=" + targets[-1].name).concretized()
    if len(targets) == 1:
        assert s.package.different_by_target() == targets[-1].name
    else:
        with pytest.raises(NoSuchMethodError):
            s.package.different_by_target()


@pytest.mark.parametrize(
    "spec_str,method_name,expected_result",
    [
        # This is overridden in the second case
        ("multimethod@3", "base_method", "multimethod"),
        ("multimethod-inheritor@3", "base_method", "multimethod-inheritor"),
        # Here we have a mix of inherited and overridden methods
        ("multimethod-inheritor@1.0", "inherited_and_overridden", "inheritor@1.0"),
        ("multimethod-inheritor@2.0", "inherited_and_overridden", "base@2.0"),
        ("multimethod@1.0", "inherited_and_overridden", "base@1.0"),
        ("multimethod@2.0", "inherited_and_overridden", "base@2.0"),
        # Diamond-like inheritance (even though the MRO linearize everything)
        ("multimethod-diamond@1.0", "diamond_inheritance", "base_package"),
        ("multimethod-base@=1.0", "diamond_inheritance", "base_package"),
        ("multimethod-diamond@2.0", "diamond_inheritance", "first_parent"),
        ("multimethod-inheritor@2.0", "diamond_inheritance", "first_parent"),
        ("multimethod-diamond@=3.0", "diamond_inheritance", "second_parent"),
        ("multimethod-diamond-parent@=3.0", "diamond_inheritance", "second_parent"),
        ("multimethod-diamond@4.0", "diamond_inheritance", "subclass"),
    ],
)
def test_multimethod_calls_and_inheritance(spec_str, method_name, expected_result):
    s = spack.spec.Spec(spec_str).concretized()
    assert getattr(s.package, method_name)() == expected_result
