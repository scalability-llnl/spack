# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REdger(RPackage):
    """Empirical Analysis of Digital Gene Expression Data in R.

    Differential expression analysis of RNA-seq expression profiles with
    biological replication. Implements a range of statistical methodology
    based on the negative binomial distributions, including empirical Bayes
    estimation, exact tests, generalized linear models and quasi-likelihood
    tests. As well as RNA-seq, it be applied to differential signal analysis
    of other types of genomic data that produce counts, including ChIP-seq,
    Bisulfite-seq, SAGE and CAGE."""

    bioc = "edgeR"

    version("3.42.0", commit="197b9a8ccc27016611b262c2c31ca22f991661c5")
    version("3.40.0", commit="0b25adcc6b3cb0a8c641964d1274536ee07ee162")
    version("3.38.4", commit="f5a3bb568a23b34146ac66329a95ee4785093536")
    version("3.38.1", commit="e58bf52f34ec451096f593126922ad7e5d517f7e")
    version("3.36.0", commit="c7db03addfc42138a1901834409c02da9d873026")
    version("3.32.1", commit="b881d801d60e5b38413d27f149384c218621c55a")
    version("3.26.8", commit="836809e043535f2264e5db8b5c0eabcffe85613f")
    version("3.24.3", commit="d1260a2aeba67b9ab7a9b8b197b746814ad0716d")
    version("3.22.5", commit="44461aa0412ef4a0d955730f365e44fc64fe1902")
    version("3.20.9", commit="acbcbbee939f399673678653678cd9cb4917c4dc")
    version("3.18.1", commit="101106f3fdd9e2c45d4a670c88f64c12e97a0495")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@3.26.8:")
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-limma@3.34.5:", type=("build", "run"), when="@3.20.9:")
    depends_on("r-limma@3.41.5:", type=("build", "run"), when="@3.32.1:")
    depends_on("r-locfit", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"), when="@3.20.9:")
