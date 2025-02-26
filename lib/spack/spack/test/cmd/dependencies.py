# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from llnl.util.tty.color import color_when

import spack.store
from spack.main import SpackCommand

dependencies = SpackCommand("dependencies")

MPIS = [
    "intel-parallel-studio",
    "low-priority-provider",
    "mpich",
    "mpich2",
    "multi-provider-mpi",
    "zmpi",
]
COMPILERS = ["gcc", "llvm"]
MPI_DEPS = ["fake"]


@pytest.mark.parametrize(
    "cli_args,expected",
    [
        (["mpileaks"], set(["callpath"] + MPIS + COMPILERS)),
        (
            ["--transitive", "mpileaks"],
            set(["callpath", "dyninst", "libdwarf", "libelf"] + MPIS + MPI_DEPS + COMPILERS),
        ),
        (["--transitive", "--deptype=link,run", "dtbuild1"], {"dtlink2", "dtrun2"}),
        (["--transitive", "--deptype=build", "dtbuild1"], {"dtbuild2", "dtlink2"}),
        (["--transitive", "--deptype=link", "dtbuild1"], {"dtlink2"}),
    ],
)
def test_direct_dependencies(cli_args, expected, mock_runtimes):
    out = dependencies(*cli_args)
    result = set(re.split(r"\s+", out.strip()))
    expected.update(mock_runtimes)
    assert expected == result


@pytest.mark.db
def test_direct_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies("--installed", "mpileaks^mpich")

    root = spack.store.STORE.db.query_one("mpileaks ^mpich")

    lines = [line for line in out.strip().split("\n") if line and not line.startswith("--")]
    hashes = {re.split(r"\s+", line)[0] for line in lines}
    expected = {s.dag_hash(7) for s in root.dependencies()}

    assert expected == hashes


@pytest.mark.db
def test_transitive_installed_dependencies(mock_packages, database):
    with color_when(False):
        out = dependencies("--installed", "--transitive", "mpileaks^zmpi")

    root = spack.store.STORE.db.query_one("mpileaks ^zmpi")

    lines = [line for line in out.strip().split("\n") if line and not line.startswith("--")]
    hashes = {re.split(r"\s+", line)[0] for line in lines}
    expected = {s.dag_hash(7) for s in root.traverse(root=False)}

    assert expected == hashes
