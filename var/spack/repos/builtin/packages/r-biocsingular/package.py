# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocsingular(RPackage):
    """Singular Value Decomposition for Bioconductor Packages.

    Implements exact and approximate methods for singular value
    decomposition and principal components analysis, in a framework that
    allows them to be easily switched within Bioconductor packages or
    workflows. Where possible, parallelization is achieved using the
    BiocParallel framework."""

    bioc = "BiocSingular"

    version("1.16.0", commit="0db9a691d4eb21551c532d8bde8f64dcc19b6c66")
    version("1.14.0", commit="6dc42b30110e498f6694f18037f991c1006c71b7")
    version("1.12.0", commit="7d1b8f4954e9e6f2c30a5111cdab9aabc8bcc3a6")
    version("1.10.0", commit="6615ae8cb124aba6507447c1081bd2eba655e57d")
    version("1.6.0", commit="11baf1080d6f791439cd5d97357589d6451643d9")
    version("1.0.0", commit="d2b091c072d0312698c9bb6611eb1bdf8aebf833")

    depends_on("cxx", type="build")  # generated

    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-delayedarray", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-scaledmatrix", type=("build", "run"), when="@1.10.0:")
    depends_on("r-irlba", type=("build", "run"))
    depends_on("r-rsvd", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-beachmat", type=("build", "run"))
