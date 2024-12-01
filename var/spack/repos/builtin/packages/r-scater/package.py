# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScater(RPackage):
    """Single-Cell Analysis Toolkit for Gene Expression Data in R.

    A collection of tools for doing various analyses of single-cell RNA-seq
    gene expression data, with a focus on quality control and
    visualization."""

    bioc = "scater"

    version("1.28.0", commit="e654498c3fa9f769b794f840f230720333bd9555")
    version("1.26.0", commit="a548ddc8424e185bfb06f48bfc174071e69fc687")
    version("1.24.0", commit="013f0935a1a225139986ca5a3f0e9d08a1558153")
    version("1.22.0", commit="ea2c95c53adb8c6fab558c1cb869e2eab36aa9f8")
    version("1.18.3", commit="a94e7f413bf0f5f527b41b0b34e7a8e5c947ae37")
    version("1.12.2", commit="1518dc27a87c79181c34107d639e95fe55e55092")
    version("1.10.1", commit="2e6694af2929092f263c2b0830d48b3f9632e70c")
    version("1.8.4", commit="d560a9a378541d53d17990d2aa2cd28874df3dcd")
    version("1.6.3", commit="964effb4e883102d7c8cae627dbac4ba5d216a75")
    version("1.4.0", commit="90a2eab66ff82ba6dd7fbb33e41cd0ded20fa218")

    depends_on("r@3.3:", type=("build", "run"), when="@1.4.0")
    depends_on("r@3.4:", type=("build", "run"), when="@1.6.3")
    depends_on("r@3.5:", type=("build", "run"), when="@1.8.4")
    depends_on("r@3.6:", type=("build", "run"), when="@1.12.2")
    depends_on("r-singlecellexperiment", type=("build", "run"), when="@1.6.3:")
    depends_on("r-scuttle", type=("build", "run"), when="@1.18.3:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"), when="@1.6.3:")
    depends_on("r-summarizedexperiment", type=("build", "run"), when="@1.6.3:")
    depends_on("r-delayedarray", type=("build", "run"), when="@1.8.4:")
    depends_on("r-delayedmatrixstats", type=("build", "run"), when="@1.8.4:")
    depends_on("r-beachmat", type=("build", "run"), when="@1.6.3:")
    depends_on("r-biocneighbors", type=("build", "run"), when="@1.12.2:")
    depends_on("r-biocsingular", type=("build", "run"), when="@1.12.2:")
    depends_on("r-biocparallel", type=("build", "run"), when="@1.10.1:")
    depends_on("r-rlang", type=("build", "run"), when="@1.18.3:")
    depends_on("r-ggbeeswarm", type=("build", "run"))
    depends_on("r-viridis", type=("build", "run"))
    depends_on("r-rtsne", type=("build", "run"), when="@1.22.0:")
    depends_on("r-rcolorbrewer", type=("build", "run"), when="@1.22.0:")
    depends_on("r-rcppml", type=("build", "run"), when="@1.24.0:")
    depends_on("r-ggrastr", type=("build", "run"), when="@1.26.0:")
    depends_on("r-pheatmap", type=("build", "run"), when="@1.26.0:")
    depends_on("r-uwot", type=("build", "run"), when="@1.26.0:")
    depends_on("r-ggrepel", type=("build", "run"), when="@1.22.0:")
    depends_on("r-densvis", type=("build", "run"), when="@1.28.0:")

    depends_on("r-biobase", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-biomart", type=("build", "run"), when="@1.4.0:1.6.3")
    depends_on("r-data-table", type=("build", "run"), when="@1.4.0:1.6.3")
    depends_on("r-dplyr", type=("build", "run"), when="@1.4.0:1.12.2")
    depends_on("r-edger", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-limma", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-matrixstats", type=("build", "run"), when="@1.4.0:1.6.3")
    depends_on("r-plyr", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-reshape2", type=("build", "run"), when="@1.4.0:1.10.1")
    depends_on("r-rhdf5", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-rjson", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-shiny", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-shinydashboard", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-tximport", type=("build", "run"), when="@1.4.0:1.8.4")
    depends_on("r-rcpp", type=("build", "run"), when="@1.6.3:1.12.2")
    depends_on("r-rcpp@0.12.14:", type=("build", "run"), when="@1.8.4:1.12.2")
    depends_on("r-rhdf5lib", type=("build", "run"), when="@1.6.3:1.10.1")
    depends_on("r-gridextra", type=("build", "run"), when="@1.18.3:1.26.0")
