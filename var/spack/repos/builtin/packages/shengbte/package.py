# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Shengbte(MakefilePackage):
    """ShengBTE is a software package for solving the Boltzmann Transport
    Equation for phonons."""

    homepage = "https://www.shengbte.org"
    url = "https://www.shengbte.org/downloads/ShengBTE-v1.1.1-8a63749.tar.bz2"

    license("GPL-3.0-only")

    version(
        "1.1.1-8a63749", sha256="43920740d19ae854c8ecae0b648acfdf1d7726ca4c2b44f1a1684457f2f88522"
    )

    depends_on("mpi")
    depends_on("spglib")
    depends_on("mkl")

    parallel = False

    build_directory = "Src"

    def edit(self, spec, prefix):
        arch_make = join_path(self.build_directory, "arch.make")
        copy("arch.make.example", arch_make)
        filter_file("export FFLAGS=.*", "export FFLAGS=-debug -O2", arch_make)
        filter_file(
            "export LDFLAGS=.*", "export LDFLAGS=" + spec["spglib"].libs.ld_flags, arch_make
        )

        filter_file("export MPIFC=.*", "export MPIFC=%s" % spec["mpi"].mpifc, arch_make)
        filter_file("LAPACK=.*", "LAPACK=" + spec["mkl"].libs.ld_flags, arch_make)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ShengBTE", prefix.bin)
