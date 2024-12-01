# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.spec import Spec


@pytest.fixture(
    params=[
        # Normalize simple conditionals
        ("optional-dep-test", {"optional-dep-test": None}),
        ("optional-dep-test~a", {"optional-dep-test~a": None}),
        ("optional-dep-test+a", {"optional-dep-test+a": {"pkg-a": None}}),
        ("optional-dep-test a=true", {"optional-dep-test a=true": {"pkg-a": None}}),
        ("optional-dep-test a=true", {"optional-dep-test+a": {"pkg-a": None}}),
        ("optional-dep-test@1.1", {"optional-dep-test@1.1": {"pkg-b": None}}),
        ("optional-dep-test%intel", {"optional-dep-test%intel": {"pkg-c": None}}),
        (
            "optional-dep-test%intel@64.1",
            {"optional-dep-test%intel@64.1": {"pkg-c": None, "pkg-d": None}},
        ),
        (
            "optional-dep-test%intel@64.1.2",
            {"optional-dep-test%intel@64.1.2": {"pkg-c": None, "pkg-d": None}},
        ),
        ("optional-dep-test%clang@35", {"optional-dep-test%clang@35": {"pkg-e": None}}),
        # Normalize multiple conditionals
        ("optional-dep-test+a@1.1", {"optional-dep-test+a@1.1": {"pkg-a": None, "pkg-b": None}}),
        (
            "optional-dep-test+a%intel",
            {"optional-dep-test+a%intel": {"pkg-a": None, "pkg-c": None}},
        ),
        (
            "optional-dep-test@1.1%intel",
            {"optional-dep-test@1.1%intel": {"pkg-b": None, "pkg-c": None}},
        ),
        (
            "optional-dep-test@1.1%intel@64.1.2+a",
            {
                "optional-dep-test@1.1%intel@64.1.2+a": {
                    "pkg-a": None,
                    "pkg-b": None,
                    "pkg-c": None,
                    "pkg-d": None,
                }
            },
        ),
        (
            "optional-dep-test@1.1%clang@36.5+a",
            {"optional-dep-test@1.1%clang@36.5+a": {"pkg-b": None, "pkg-a": None, "pkg-e": None}},
        ),
        # Chained MPI
        (
            "optional-dep-test-2+mpi",
            {"optional-dep-test-2+mpi": {"optional-dep-test+mpi": {"mpi": None}}},
        ),
        # Each of these dependencies comes from a conditional
        # dependency on another.  This requires iterating to evaluate
        # the whole chain.
        (
            "optional-dep-test+f",
            {"optional-dep-test+f": {"pkg-f": None, "pkg-g": None, "mpi": None}},
        ),
    ]
)
def spec_and_expected(request):
    """Parameters for the normalization test."""
    spec, d = request.param
    return spec, Spec.from_literal(d)


def test_default_variant(config, mock_packages):
    spec = Spec("optional-dep-test-3")
    spec.concretize()
    assert "pkg-a" in spec

    spec = Spec("optional-dep-test-3~var")
    spec.concretize()
    assert "pkg-a" in spec

    spec = Spec("optional-dep-test-3+var")
    spec.concretize()
    assert "pkg-b" in spec
