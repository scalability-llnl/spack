# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RS4arrays(RPackage):
    """Foundation of array-like containers in Bioconductor."""

    bioc = "S4Arrays"

    version("1.7.1", commit="7081384e789c081b337a3867040d052d93adfb11")

    depends_on("r@4.3.0:", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-biocgenerics@0.45.2:", type=("build", "run"))
    depends_on("r-crayon", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
