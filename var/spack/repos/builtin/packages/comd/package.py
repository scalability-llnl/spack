# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Comd(MakefilePackage):
    """CoMD is a reference implementation of classical molecular dynamics
    algorithms and workloads as used in materials science. It is created and
    maintained by The Exascale Co-Design Center for Materials in Extreme
    Environments (ExMatEx). The code is intended to serve as a vehicle for
    co-design by allowing others to extend and/or reimplement it as needed to
    test performance of new architectures, programming models, etc. New
    versions of CoMD will be released to incorporate the lessons learned from
    the co-design process."""

    tags = ["proxy-app"]

    homepage = "http://www.exmatex.org/comd.html"
    url = "https://github.com/ECP-copa/CoMD/archive/v1.1.tar.gz"
    git = "https://github.com/ECP-copa/CoMD.git"

    version("develop", branch="master")
    version("1.1", sha256="4e85f86f043681a1ef72940fc24a4c71356a36afa45446f7cfe776abad6aa252")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("precision", default=True, description="Toggle Precesion Options")
    variant("graphs", default=False, description="Enable graph visuals")

    depends_on("mpi", when="+mpi")
    depends_on("graphviz", when="+graphs")

    conflicts("+openmp", when="+mpi")

    def edit(self, spec, prefix):
        with working_dir("src-mpi") or working_dir("src-openmp"):
            copy("Makefile.vanilla", "Makefile")

    @property
    def build_targets(self):
        targets = []
        cflags = " -std=c99 "
        optflags = " -g -O5 "
        clib = " -lm "
        comd_variant = "CoMD"
        cc = spack_cc

        if self.spec.satisfies("+openmp"):
            targets.append("--directory=src-openmp")
            comd_variant += "-openmp"
            cflags += " -fopenmp "
            if self.spec.satisfies("+mpi"):
                comd_variant += "-mpi"
                targets.append("CC = {0}".format(self.spec["mpi"].mpicc))
            else:
                targets.append("CC = {0}".format("spack_cc"))

        else:
            targets.append("--directory=src-mpi")
            if self.spec.satisfies("~mpi"):
                comd_variant += "-serial"
                targets.append("CC = {0}".format(cc))
            else:
                comd_variant += "-mpi"
                targets.append("CC = {0}".format(self.spec["mpi"].mpicc))
        if self.spec.satisfies("+mpi"):
            cflags += "-DDO_MPI"
            targets.append("INCLUDES = {0}".format(self.spec["mpi"].prefix.include))

        if self.spec.satisfies("+precision"):
            cflags += " -DDOUBLE "
        else:
            cflags += " -DSINGLE "

        targets.append("CoMD_VARIANT = {0}".format(comd_variant))
        targets.append("CFLAGS = {0}".format(cflags))
        targets.append("OPTFLAGS = {0}".format(optflags))
        targets.append("C_LIB = {0}".format(clib))

        return targets

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("examples", prefix.examples)
        install_tree("pots", prefix.pots)
        mkdirp(prefix.doc)
        install("README.md", prefix.doc)
        install("LICENSE.md", prefix.doc)
