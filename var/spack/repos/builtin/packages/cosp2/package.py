# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cosp2(MakefilePackage):
    """Proxy Application. CoSP2 represents a sparse linear algebra
    parallel algorithm for calculating the density matrix in electronic
    tructure theory. The algorithm is based on a recursive second-order
    Fermi-Operator expansion method (SP2) and is tailored for density
    functional based tight-binding calculations of non-metallic systems.
    """

    tags = ["proxy-app"]

    homepage = "http://www.exmatex.org/cosp2.html"
    git = "https://github.com/exmatex/CoSP2.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    variant("double", default=True, description="Build with double precision.")
    variant("mpi", default=True, description="Build with MPI Support")

    depends_on("mpi", when="+mpi")

    build_directory = "src-mpi"

    def edit(self, spec, prefix):
        cc = spack_cc

        if spec.satisfies("+mpi"):
            cc = spec["mpi"].mpicc

        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile.vanilla")
            makefile.filter(r"^CC\s*=.*", "CC = {0}".format(cc))

            if spec.satisfies("+double"):
                filter_file("DOUBLE_PRECISION = O.*", "DOUBLE_PRECISION = OFF", "Makefile.vanilla")
            copy("Makefile.vanilla", "Makefile")

    def install(self, spec, prefix):
        install_tree("bin/", prefix.bin)
        install_tree("examples/", prefix.examples)
        install_tree("doc/", prefix.doc)
        install("src-mpi/Doxyfile", prefix.doc)
        install("README.md", prefix.doc)
        install("LICENSE.md", prefix.doc)
