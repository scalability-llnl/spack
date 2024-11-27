# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAda(RPackage):
    """The R Package Ada for Stochastic Boosting.

    Performs discrete, real, and gentle boost under both exponential and
    logistic loss on a given data set. The package ada provides a
    straightforward, well-documented, and broad boosting routine for
    classification, ideally suited for small to moderate-sized data sets."""

    cran = "ada"

    license("GPL-2.0-or-later")

    version("2.0-5", sha256="d900172059eebeef30c27944fc29737a231fc4f92e3c2661868383fbd9016ac0")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
