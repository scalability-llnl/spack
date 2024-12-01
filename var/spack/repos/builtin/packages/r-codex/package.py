# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCodex(RPackage):
    """A Normalization and Copy Number Variation Detection Method for Whole
    Exome Sequencing.

    A normalization and copy number variation calling procedure for whole
    exome DNA sequencing data. CODEX relies on the availability of multiple
    samples processed using the same sequencing pipeline for normalization, and
    does not require matched controls. The normalization model in CODEX
    includes terms that specifically remove biases due to GC content, exon
    length and targeting and amplification efficiency, and latent systemic
    artifacts. CODEX also includes a Poisson likelihood-based recursive
    segmentation procedure that explicitly models the count-based exome
    sequencing data."""

    bioc = "CODEX"

    version("1.32.0", commit="83926238fb49b0e95d989612a98356d20e7caf57")
    version("1.30.0", commit="0694f11be9e0b02ab15047d01db2afce943f92d8")
    version("1.28.0", commit="c707497bd93aa4a0516fcf3671a64997c28c9f67")
    version("1.26.0", commit="729fd10bd42d12edcedd65b5a8fb1579e5949718")
    version("1.22.0", commit="aa0ee4278111a46e0c790312b0526ba07aab22eb")
    version("1.18.0", commit="9a95cccc7ff3fe587636317e21e39a07dddf80bc")

    depends_on("r@3.2.3:", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-bsgenome-hsapiens-ucsc-hg19", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
