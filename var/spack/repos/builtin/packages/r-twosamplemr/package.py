# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTwosamplemr(RPackage):
    """Two Sample MR functions and interface to MR Base database.

    A package for performing Mendelian randomization using GWAS summary data.
    It uses the IEU GWAS database to obtain data automatically, and a wide
    range of methods to run the analysis. You can use the MR-Base web app to
    try out a limited range of the functionality in this package, but for any
    serious work we strongly recommend using this R package."""

    homepage = "https://mrcieu.github.io/TwoSampleMR/"
    url = "https://github.com/MRCIEU/TwoSampleMR/archive/refs/tags/v0.5.6.tar.gz"

    license("MIT")

    version("0.5.6", sha256="c63eb008ab7ed08a6f30ccbf0c299beb31b2f5835e5e2aa1b59c5e4fe284a30c")

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r-ieugwasr@0.1.5:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-cowplot", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-markdown", type=("build", "run"))
    depends_on("r-gtable", type=("build", "run"))
    depends_on("r-rmarkdown", type=("build", "run"))
    depends_on("r-mendelianrandomization", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-mr-raps", type=("build", "run"))
    depends_on("r-psych", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-car", type=("build", "run"))
    depends_on("r-randomforest", type=("build", "run"))
    depends_on("r-meta", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-mrpresso", type=("build", "run"))
    depends_on("r-mrinstruments", type=("build", "run"))
    depends_on("r-radialmr", type=("build", "run"))
    depends_on("r-mrmix", type=("build", "run"))
    depends_on("r-glmnet", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-pbapply", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
