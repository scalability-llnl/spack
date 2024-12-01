# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAneufinder(RPackage):
    """Analysis of Copy Number Variation in Single-Cell-Sequencing Data.

    AneuFinder implements functions for copy-number detection, breakpoint
    detection, and karyotype and heterogeneity analysis in single-cell whole
    genome sequencing and strand-seq data."""

    bioc = "AneuFinder"

    version("1.28.0", commit="e17d810171bdab1c6a26a3ab7b7931db4e073e7e")
    version("1.26.0", commit="7cd59a1e24c6512f2e4fcbe2c53a0d3cd2d06217")
    version("1.24.0", commit="4c6906eee514eba3e8ac159654a6953e37a99bba")
    version("1.22.0", commit="ea0beb3d827c2dd4bc56708a839a93c55304918b")
    version("1.18.0", commit="76ec9af947f97212084ca478e8e82f9e0eb79de9")
    version("1.12.1", commit="e788fd0c864f0bf0abd93df44c6d42f82eb37e0e")
    version("1.10.2", commit="56578ae69abac93dfea6bcac1fc205b14b6ba9dd")
    version("1.8.0", commit="36a729d244add5aafbe21c37a1baaea6a50354d3")
    version("1.6.0", commit="0cfbdd1951fb4df5622e002260cfa86294d65d1d")
    version("1.4.0", commit="e5bdf4d5e4f84ee5680986826ffed636ed853b8e")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.10.2:")
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-cowplot", type=("build", "run"))
    depends_on("r-aneufinderdata", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"), when="@1.4.0:")
    depends_on("r-biocgenerics@0.31.6:", type=("build", "run"), when="@1.18.0:")
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-bamsignals", type=("build", "run"))
    depends_on("r-dnacopy", type=("build", "run"))
    depends_on("r-ecp", type=("build", "run"), when="@1.8.0:")
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-genomicalignments", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-ggdendro", type=("build", "run"))
    depends_on("r-ggrepel", type=("build", "run"))
    depends_on("r-mclust", type=("build", "run"))
    depends_on("r-reordercluster", type=("build", "run"), when="@:1.26.0")
