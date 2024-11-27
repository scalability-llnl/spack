# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wgsim(Package):
    """Wgsim is a small tool for simulating sequence reads from a reference
    genome.

    It is able to simulate diploid genomes with SNPs and insertion/deletion
    (INDEL) polymorphisms, and simulate reads with uniform substitution
    sequencing errors. It does not generate INDEL sequencing errors, but this
    can be partly compensated by simulating INDEL polymorphisms."""

    homepage = "https://github.com/lh3/wgsim"
    git = "https://github.com/lh3/wgsim.git"

    version("2011.10.17", commit="a12da3375ff3b51a5594d4b6fa35591173ecc229")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        cc = Executable(spack_cc)
        cc("-g", "-O2", "-Wall", "-o", "wgsim", "wgsim.c", "-lz", "-lm")

        install_tree(self.stage.source_path, prefix.bin)
