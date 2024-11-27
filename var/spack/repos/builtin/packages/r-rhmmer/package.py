# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRhmmer(RPackage):
    """Utilities Parsing 'HMMER' Results.

    'HMMER' is a profile hidden Markov model tool used primarily for sequence
    analysis in bioinformatics (<http://hmmer.org/>). 'rhmmer' provides
    utilities for parsing the 'HMMER' output into tidy data frames."""

    cran = "rhmmer"

    version("0.1.0", sha256="5022cefc9ba335160c1ad8d1b614610ae0ad48287c9fdbaf8f8966149358e520")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-readr", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
