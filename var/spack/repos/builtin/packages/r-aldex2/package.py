# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAldex2(RPackage):
    """Analysis Of Differential Abundance Taking Sample Variation Into Account.

    A differential abundance analysis for the comparison of two or more
    conditions. Useful for analyzing data from standard RNA-seq or meta-RNA-
    seq assays as well as selected and unselected values from in-vitro
    sequence selections. Uses a Dirichlet-multinomial model to infer
    abundance from counts, optimized for three or more experimental
    replicates. The method infers biological and sampling variation to
    calculate the expected false discovery rate, given the variation, based
    on a Wilcoxon Rank Sum test and Welch's t-test (via aldex.ttest), a
    Kruskal-Wallis test (via aldex.kw), a generalized linear model (via
    aldex.glm), or a correlation test (via aldex.corr). All tests report
    p-values and Benjamini-Hochberg corrected p-values."""

    bioc = "ALDEx2"

    license("GPL-3.0-only")

    version("1.32.0", commit="ba32b9a9b6a8f42906ea094318f00116f15e42eb")
    version("1.30.0", commit="cb6670515a8722f9cfedac12a8c2747a5298ee46")
    version("1.28.1", commit="f8d8ba6d2439bff75ab80f5466c9a047c31ed0a6")
    version("1.26.0", commit="0876a2eac08d3f1c01df7414d97d391c80182ada")
    version("1.22.0", commit="ac7f0ab3f094ec52713da7620a27058b14c7181d")
    version("1.16.0", commit="bd698a896a5bea91187e3060e56a147bad1d586f")
    version("1.14.1", commit="a8b970c594a00a37c064227bf312d5f89dccabe8")
    version("1.12.0", commit="9efde428d22a0be1fe7b6655d45ddce8fcded180")
    version("1.10.0", commit="e43f99e4009ad4d5ed200cc8a19faf7091c0c98a")
    version("1.8.0", commit="24104824ca2402ad4f54fbf1ed9cee7fac2aaaf1")

    depends_on("r-zcompositions", type=("build", "run"), when="@1.22.0:")
    depends_on("r-rfast", type=("build", "run"), when="@1.26.0:")
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-multtest", type=("build", "run"), when="@1.10.0:")
