# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFactoextra(RPackage):
    """Extract and Visualize the Results of Multivariate Data Analyses.

    Provides some easy-to-use functions to extract and visualize the output of
    multivariate data analyses, including 'PCA' (Principal Component Analysis),
    'CA' (Correspondence Analysis), 'MCA' (Multiple Correspondence Analysis),
    'FAMD' (Factor Analysis of Mixed Data), 'MFA' (Multiple Factor Analysis)
    and 'HMFA' (Hierarchical Multiple Factor Analysis) functions from different
    R packages. It contains also functions for simplifying some clustering
    analysis steps and provides 'ggplot2' - based elegant data
    visualization."""

    cran = "factoextra"

    license("GPL-2.0-only")

    version("1.0.7", sha256="624ff01c74933352aca55966f8a052b1ccc878f52c2c307e47f88e0665db94aa")
    version("1.0.5", sha256="8177a3f5107883ae248b2cd0afa388a1794741f5155a9455b3883788cf44d5d0")
    version("1.0.4", sha256="e4a000a04ef5b9aa0790dc6e5277451c482a19ba10dda9474f6c6982424aeed3")

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.0:", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-dendextend", type=("build", "run"))
    depends_on("r-factominer", type=("build", "run"))
    depends_on("r-ggpubr@0.1.5:", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-ggrepel", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
