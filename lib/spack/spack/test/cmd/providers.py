# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

from spack.main import SpackCommand

providers = SpackCommand("providers")


@pytest.mark.parametrize(
    "pkg",
    [("mpi",), ("mpi@2",), ("mpi", "lapack"), ("",)],  # Lists all the available virtual packages
)
def test_it_just_runs(pkg):
    providers(*pkg)


@pytest.mark.parametrize(
    "vpkg,provider_list",
    [
        (
            ("mpi",),
            [
                "intel-mpi",
                "intel-parallel-studio",
                "mpich",
                "mpilander",
                "mvapich2",
                "openmpi",
                "openmpi@1.7.5:",
                "openmpi@2.0.0:",
                "spectrum-mpi",
            ],
        ),
        (("D", "awk"), ["ldc", "gawk", "mawk"]),  # Call 2 virtual packages at once
    ],
)
def test_provider_lists(vpkg, provider_list):
    output = providers(*vpkg)
    for item in provider_list:
        assert item in output


@pytest.mark.parametrize(
    "pkg,error_cls",
    [
        ("zlib", ValueError),
        ("foo", ValueError),  # Trying to call with a package that does not exist
    ],
)
def test_it_just_fails(pkg, error_cls):
    with pytest.raises(error_cls):
        providers(pkg)
