# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fermi(MakefilePackage):
    """A WGS de novo assembler based on the FMD-index for large genomes."""

    homepage = "https://github.com/lh3/fermi"
    url = "https://github.com/downloads/lh3/fermi/fermi-1.1.tar.bz2"

    version("1.1", sha256="f1351b52a4ff40e5d708899e90ecf747e7af8d4eac795f6968e5b58c2ba11a67")

    depends_on("zlib-api")
    depends_on("perl", type="run")
    depends_on("sse2neon", when="target=aarch64:")

    patch("ksw_for_aarch64.patch", when="target=aarch64:")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("fermi", prefix.bin)
        install("run-fermi.pl", prefix.bin)
