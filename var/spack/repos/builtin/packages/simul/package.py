# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Simul(Package):
    """simul is an MPI coordinated test of parallel
    filesystem system calls and library functions."""

    homepage = "https://github.com/LLNL/simul"
    url = "https://github.com/LLNL/simul/archive/1.16.tar.gz"

    version("1.16", sha256="63fce55346b22113f05efe3d1ca6ddbaea5abb959e28b24c6821bce949859a9b")
    version("1.15", sha256="39a2458cd31c9266c58effd598611c610c5a2616ca6a7318f76830d203f3783f")
    version("1.14", sha256="cbc70881b2a03e9a5076dbdf82b6fdfa48351ab381e379935b9c7db0ee315c92")
    version("1.13", sha256="42a67258181fbf723cfe13d4d2dabc5aed0d0daa606b9d817108c354e37d1c64")

    depends_on("c", type="build")  # generated

    depends_on("mpi")

    def install(self, spec, prefix):
        filter_file("mpicc", "$(MPICC)", "Makefile", string=True)
        filter_file("inline void", "void", "simul.c", string=True)
        make("simul")
        mkdirp(prefix.bin)
        install("simul", prefix.bin)
