# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsamtools(RPackage):
    """Binary alignment (BAM), FASTA, variant call (BCF), and tabix file
    import.

    This package provides an interface to the 'samtools', 'bcftools', and
    'tabix' utilities for manipulating SAM (Sequence Alignment / Map),
    FASTA, binary variant call (BCF) and compressed indexed tab-delimited
    (tabix) files."""

    bioc = "Rsamtools"

    license("MIT")

    version("2.16.0", commit="3eb6d03acecb8d640ec5201cacdc322e9e0c2445")
    version("2.14.0", commit="8302eb7fa1c40384f1af5855222d94f2efbdcad1")
    version("2.12.0", commit="d6a65dd57c5a17e4c441a27492e92072f69b175e")
    version("2.10.0", commit="b19738e85a467f9032fc7903be3ba10e655e7061")
    version("2.6.0", commit="f2aea061517c5a55e314c039251ece9831c7fad2")
    version("2.2.1", commit="f10084658b4c9744961fcacd79c0ae9a7a40cd30")
    version("2.0.3", commit="17d254cc026574d20db67474260944bf60befd70")
    version("1.34.1", commit="0ec1d45c7a14b51d019c3e20c4aa87c6bd2b0d0c")
    version("1.32.3", commit="0aa3f134143b045aa423894de81912becf64e4c2")
    version("1.30.0", commit="61b365fe3762e796b3808cec7238944b7f68d7a6")
    version("1.28.0", commit="dfa5b6abef68175586f21add7927174786412472")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.5.0:", type=("build", "run"), when="@2.10.0:")
    depends_on("r-genomeinfodb@1.1.3:", type=("build", "run"))
    depends_on("r-genomicranges@1.21.6:", type=("build", "run"))
    depends_on("r-genomicranges@1.31.8:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-biostrings@2.37.1:", type=("build", "run"))
    depends_on("r-biostrings@2.47.6:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-biocgenerics@0.1.3:", type=("build", "run"))
    depends_on("r-biocgenerics@0.25.1:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-s4vectors@0.13.8:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.25:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-iranges@2.3.7:", type=("build", "run"))
    depends_on("r-iranges@2.13.12:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-xvector@0.15.1:", type=("build", "run"))
    depends_on("r-xvector@0.19.7:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-zlibbioc", type=("build", "run"))
    depends_on("r-bitops", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-rhtslib@1.16.3", type=("build", "run"), when="@2.0.3")
    depends_on("r-rhtslib@1.17.7:", type=("build", "run"), when="@2.2.1:")
    depends_on("r-rhtslib@1.99.3:", type=("build", "run"), when="@2.14.0:")
    depends_on("gmake", type="build")

    # this is not a listed dependency but is needed
    depends_on("curl")
