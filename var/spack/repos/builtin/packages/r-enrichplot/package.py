# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REnrichplot(RPackage):
    """Visualization of Functional Enrichment Result.

    The 'enrichplot' package implements several visualization methods for
    interpreting functional enrichment results obtained from ORA or GSEA
    analysis. All the visualization methods are developed based on 'ggplot2'
    graphics."""

    bioc = "enrichplot"

    version("1.20.0", commit="ae72efe5f2ded561958f95bc8b1b41c0fc79840e")
    version("1.18.0", commit="61ea941784a1ed6cc604af1c1cc4532b8b5fcea7")
    version("1.16.2", commit="eeb21345288d96c116ac308649fa772d03760259")
    version("1.16.1", commit="cff77b622b2312be546714ec437aa4bc585bac87")
    version("1.14.1", commit="ccf3a6d9b7cd9cffd8de6d6263efdffe59d2ec36")
    version("1.10.2", commit="77ee04f60a07cc31151f8f47f8ee64f3a43c9760")
    version("1.4.0", commit="6ffe5d9c5dbe5cbea29f2e0941595475bbbcea0e")
    version("1.2.0", commit="2eeaafb571d35a106eba8ae7df014f3201066e8b")
    version("1.0.2", commit="ba7726fa0d4b581b7514dcbb04889cdbdd75ff29")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.10.2:")
    depends_on("r-aplot", type=("build", "run"), when="@1.14.1:")
    depends_on("r-aplot@0.1.4:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-dose@3.5.1:", type=("build", "run"))
    depends_on("r-dose@3.13.1:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-dose@3.16.0:", type=("build", "run"), when="@1.12.3:")
    depends_on("r-ggnewscale", type=("build", "run"), when="@1.18.0:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-ggraph", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"), when="@1.10.2:")
    depends_on("r-purrr", type=("build", "run"), when="@1.2.0:")
    depends_on("r-rcolorbrewer", type=("build", "run"), when="@1.2.0:")
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.18.0:")
    depends_on("r-scatterpie", type=("build", "run"), when="@1.10.2:")
    depends_on("r-shadowtext", type=("build", "run"), when="@1.10.2:")
    depends_on("r-gosemsim", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"), when="@1.10.2:")
    depends_on("r-ggtree", type=("build", "run"), when="@1.14.1:")
    depends_on("r-yulab-utils@0.0.4:", type=("build", "run"), when="@1.14.1:")

    depends_on("r-ggridges", type=("build", "run"), when="@:1.4.0")
    depends_on("r-upsetr", type=("build", "run"), when="@:1.4.0")
    depends_on("r-annotationdbi", type=("build", "run"), when="@:1.4.0")
    depends_on("r-europepmc", type=("build", "run"), when="@1.2.0:1.4.0")
    depends_on("r-ggplotify", type=("build", "run"), when="@1.2.0:1.4.0")
    depends_on("r-gridextra", type=("build", "run"), when="@1.2.0:1.4.0")
    depends_on("r-cowplot", type=("build", "run"), when="@:1.16.1")
