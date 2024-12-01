# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSseq(RPackage):
    """Shrinkage estimation of dispersion in Negative Binomial models for RNA-
    seq experiments with small sample size.

    The purpose of this package is to discover the genes that are
    differentially expressed between two conditions in RNA-seq experiments.
    Gene expression is measured in counts of transcripts and modeled with
    the Negative Binomial (NB) distribution using a shrinkage approach for
    dispersion estimation. The method of moment (MM) estimates for
    dispersion are shrunk towards an estimated target, which minimizes the
    average squared difference between the shrinkage estimates and the
    initial estimates. The exact per-gene probability under the NB model is
    calculated, and used to test the hypothesis that the expected expression
    of a gene in two conditions identically follow a NB distribution."""

    bioc = "sSeq"

    version("1.38.0", commit="09242bb94d72ff13e3f18c3588934149f27ac374")
    version("1.36.0", commit="0345ac579c4bdcc9c42c24831ad86fc6225c5cb9")
    version("1.34.0", commit="882bea1664f55d85550a7185cbd4a0108c35df36")
    version("1.32.0", commit="c0d3c305755d888f64d334a4ab5fa54c623054cf")
    version("1.28.0", commit="401f6805628bdf6579cc0e643b7ed54319f024be")
    version("1.22.0", commit="fa3895c9578edddca17b5d13a2678ee5830b85cc")
    version("1.20.1", commit="91f31440323612cb04beb44404ab0a1bcb3ad87d")
    version("1.18.0", commit="1f65e5a55ce0d51672b785450031872e6db5ca0f")
    version("1.16.0", commit="b7f2b99dbd4a12ee9d18b0ec9898f13f1038479e")
    version("1.14.0", commit="20ccffeb60196914975aa1feef902ddba659c571")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-catools", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
