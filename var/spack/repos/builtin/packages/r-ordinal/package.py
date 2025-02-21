# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROrdinal(RPackage):
    """Regression Models for Ordinal Data.

    Implementation of cumulative link (mixed) models also known as ordered
    regression models, proportional odds models, proportional hazards models
    for grouped survival times and ordered logit/probit/... models. Estimation
    is via maximum likelihood and mixed models are fitted with the Laplace
    approximation and adaptive Gauss-Hermite quadrature. Multiple random effect
    terms are allowed and they may be nested, crossed or partially
    nested/crossed. Restrictions of symmetry and equidistance can be imposed on
    the thresholds (cut-points/intercepts). Standard model methods are
    available (summary, anova, drop-methods, step, confint, predict etc.) in
    addition to profile methods and slice methods for visualizing the
    likelihood function and checking convergence."""

    cran = "ordinal"

    license("GPL-2.0-or-later")

    version(
        "2023.12-4.1", sha256="2c9dcfa438c964ff1825033d0759d25f404a2a4c5252b81e40f19cffc18e38b1"
    )
    version(
        "2022.11-16", sha256="5488ad1dfa531a09d017d68d7393d376c8bc49cceeaa6a3e5f7d57b99168d493"
    )
    version(
        "2019.12-10", sha256="7a41e7b7e852a8fa3e911f8859d36e5709ccec5ca42ee3de14a813b7aaac7725"
    )
    version("2019.4-25", sha256="2812ad7a123cae5dbe053d1fe5f2d9935afc799314077eac185c844e3c9d79df")

    depends_on("r@2.13.0:", type=("build", "run"))
    depends_on("r-ucminf", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"), when="@2022.11-16:")
