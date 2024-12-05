# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Price(MakefilePackage):
    """PRICE (Paired-Read Iterative Contig Extension): a de novo genome
    assembler implemented in C++."""

    homepage = "http://derisilab.ucsf.edu/software/price/"
    url = "https://derisilab.ucsf.edu/software/price/PriceSource140408.tar.gz"

    version("140408", sha256="12276b2b15f4e020a772944a19fd2aaf089d3437cbc71e7486fa8db95014843f")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("PriceTI", prefix.bin)
        install("PriceSeqFilter", prefix.bin)
