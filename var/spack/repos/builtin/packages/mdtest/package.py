# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mdtest(Package):
    """mdtest is an MPI-coordinated metadata benchmark test
    that performs open/stat/close operations on files
    and directories and then reports the performance."""

    homepage = "https://github.com/LLNL/mdtest"
    git = "https://github.com/LLNL/mdtest.git"

    version("1.9.3", commit="49f3f047c254c62848c23226d6f1afa5fc3c6583")

    depends_on("c", type="build")  # generated

    depends_on("mpi")

    def install(self, spec, prefix):
        filter_file("$(CC.$(OS))", spec["mpi"].mpicc, "Makefile", string=True)
        make("mdtest")
        mkdirp(prefix.bin)
        install("mdtest", prefix.bin)
