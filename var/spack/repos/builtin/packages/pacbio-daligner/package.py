# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PacbioDaligner(MakefilePackage):
    """Daligner: The Dazzler "Overlap" Module. This is a special fork
    required for some pacbio utilities."""

    homepage = "https://github.com/PacificBiosciences/DALIGNER"
    git = "https://github.com/PacificBiosciences/DALIGNER.git"

    version("2017-08-05", commit="0fe5240d2cc6b55bf9e04465b700b76110749c9d")

    depends_on("c", type="build")  # generated

    depends_on("gmake", type="build")
    depends_on("pacbio-dazz-db")

    def edit(self, spec, prefix):
        mkdir(prefix.bin)
        makefile = FileFilter("Makefile")
        makefile.filter(r"DEST_DIR\s*=\s*~/bin", "DEST_DIR = " + prefix.bin)
        gmf = FileFilter("GNUmakefile")
        gmf.filter(r"rsync\s*-av\s*\$\{ALL\}\s*\$\{PREFIX\}/bin", "cp ${ALL} " + prefix.bin)
