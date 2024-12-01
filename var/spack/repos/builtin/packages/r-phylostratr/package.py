# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhylostratr(RPackage):
    """Predict and explore the age of genes using phylostratigraphic methods"""

    homepage = "https://github.com/arenasee/phylostratr"
    git = "https://github.com/arendsee/phylostratr.git"

    license("GPL-3.0-or-later")

    version("20190323", commit="9f6d1ee2e93d973dabcfc72a44af9a032cb7ebbd")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-readr", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-rhmmer", type=("build", "run"))
    depends_on("r-rlang@0.1.2:", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-taxizedb", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
