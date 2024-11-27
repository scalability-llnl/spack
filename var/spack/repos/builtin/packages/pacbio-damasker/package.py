# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PacbioDamasker(MakefilePackage):
    """Damasker: The Dazzler Repeat Masking Suite. This is a special fork
    required for some pacbio utilities."""

    homepage = "https://github.com/PacificBiosciences/DAMASKER"
    git = "https://github.com/PacificBiosciences/DAMASKER.git"

    version("2017-02-11", commit="144244b77d52cb785cb1b3b8ae3ab6f3f0c63264")

    depends_on("c", type="build")  # generated

    depends_on("gmake", type="build")

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        makefile = FileFilter("Makefile")
        makefile.filter(r"DEST_DIR\s*=\s*~/bin", "DEST_DIR = " + prefix.bin)
        gmf = FileFilter("GNUmakefile")
        gmf.filter(r"rsync\s*-av\s*\$\{ALL\}\s*\$\{PREFIX\}/bin", "cp ${ALL} " + prefix.bin)
