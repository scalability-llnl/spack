# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTximport(RPackage):
    """Import and summarize transcript-level estimates for transcript- and
    gene-level analysis.

    Imports transcript-level abundance, estimated counts and transcript
    lengths, and summarizes into matrices for use with downstream gene-level
    analysis packages. Average transcript length, weighted by sample-
    specific transcript abundance estimates, is provided as a matrix which
    can be used as an offset for different expression of gene-level
    counts."""

    bioc = "tximport"

    version("1.28.0", commit="9acd3640c034655ffba12044ed2982fab57d4fbb")
    version("1.26.0", commit="5ae7139edf9d3445210ea014026813fd030212a8")
    version("1.24.0", commit="58524f39bdd55299cfe80a726f99b714b724be20")
    version("1.22.0", commit="335213baee3492fbf6baaa8b4e067ac0ef384684")
    version("1.18.0", commit="58b20cbc566648586b6990b30ebc70bef308cb05")
    version("1.12.3", commit="acbdead961471c3b910d720f73bd0af1b7a07c57")
    version("1.10.1", commit="cd8f81cf7140f61d4a4f25f89451fb49e2cd4bd3")
    version("1.8.0", commit="cc91b8389ca4c16b0f588bdeb63d051a11e8a705")
    version("1.6.0", commit="0b1ba6c6622e02b954812c88454c28e8efb75e0b")
    version("1.4.0", commit="bfbd2436eca21acf212b76a658b49cfb5e116d6b")
