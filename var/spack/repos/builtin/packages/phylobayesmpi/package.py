# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Phylobayesmpi(MakefilePackage):
    """Phylobayes MPI version"""

    homepage = "https://github.com/bayesiancook/pbmp"
    url = "https://github.com/bayesiancook/pbmpi/archive/v1.8b.tar.gz"
    git = "https://github.com/bayesiancook/pbmpi.git"

    license("GPL-2.0-only")

    version("1.9", sha256="567d8db995f23b2b0109c1e6088a7e5621e38fec91d6b2f27abd886b90ea31ce")
    version("1.8b", sha256="7ff017bf492c1d8b42bfff3ee8e998ba1c50f4e4b3d9d6125647b91738017324")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")

    build_directory = "sources"

    def edit(self, spec, prefix):
        with working_dir("sources"):
            makefile = FileFilter("Makefile")
            makefile.filter("CC=.*", "CC = " + spec["mpi"].mpicxx)

    def install(self, spec, prefix):
        # no install target provided in Makefile so copy the executables
        # from the data directory

        install_tree("data", prefix.bin)
