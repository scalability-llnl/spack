# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from llnl.util.tty.color import color_when

import spack.store
from spack.main import SpackCommand

dependencies = SpackCommand("dependencies")

mpis = [
    "intel-parallel-studio",
    "low-priority-provider",
    "mpich",
    "mpich2",
    "multi-provider-mpi",
    "zmpi",
]
mpi_deps = ["fake"]


def test_direct_dependencies(mock_packages):
    out = dependencies("mpileaks")
    actual = set(re.split(r"\s+", out.strip()))
    expected = set(["callpath"] + mpis)
    assert expected == actual


def test_transitive_dependencies(mock_packages):
    out = dependencies("--transitive", "mpileaks")
    actual = set(re.split(r"\s+", out.strip()))
    expected = set(["callpath", "dyninst", "libdwarf", "libelf"] + mpis + mpi_deps)
    assert expected == actual


def test_transitive_dependencies_with_deptypes(mock_packages):
    out = dependencies("--transitive", "--deptype=link,run", "dtbuild1")
    deps = set(re.split(r"\s+", out.strip()))
    assert set(["dtlink2", "dtrun2"]) == deps

    out = dependencies("--transitive", "--deptype=build", "dtbuild1")
    deps = set(re.split(r"\s+", out.strip()))
    assert set(["dtbuild2", "dtlink2"]) == deps

    out = dependencies("--transitive", "--deptype=link", "dtbuild1")
    deps = set(re.split(r"\s+", out.strip()))
    assert set(["dtlink2"]) == deps


@pytest.mark.db
def test_direct_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies("--installed", "mpileaks^mpich")

    lines = [line for line in out.strip().split("\n") if not line.startswith("--")]
    hashes = set([re.split(r"\s+", line)[0] for line in lines])

    expected = set(
        [spack.store.STORE.db.query_one(s).dag_hash(7) for s in ["mpich", "callpath^mpich"]]
    )

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies("--installed", "--transitive", "mpileaks^zmpi")

    lines = [line for line in out.strip().split("\n") if not line.startswith("--")]
    hashes = set([re.split(r"\s+", line)[0] for line in lines])

    expected = set(
        [
            spack.store.STORE.db.query_one(s).dag_hash(7)
            for s in ["zmpi", "callpath^zmpi", "fake", "dyninst", "libdwarf", "libelf"]
        ]
    )

    assert expected == hashes
