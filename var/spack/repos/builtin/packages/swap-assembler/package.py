# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SwapAssembler(MakefilePackage):
    """A scalable and fully parallelized genome assembler."""

    homepage = "https://sourceforge.net/projects/swapassembler/"
    url = (
        "https://sourceforge.net/projects/swapassembler/files/SWAP_Assembler-0.4.tar.bz2/download"
    )

    version("0.4", sha256="45632e25578aacfbacd76df9697cbc798e09ac92284d9c9c07be15e0eb348e0d")

    depends_on("cxx", type="build")  # generated

    depends_on("mpich")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("$(CC) -O2", "$(CC) -pthread -O2", string=True)

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
