# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RArm(RPackage):
    """Functions to accompany A. Gelman and J. Hill, Data Analysis Using
    Regression and Multilevel/Hierarchical Models, Cambridge University
    Press, 2007."""

    homepage = "https://github.com/suyusung/arm"
    cran = "arm"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("1.14-4", sha256="425bcb0afea2efb668d15ed8daa430bb356c62587eba806fd91e37afac1807bd")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-matrix@1.0:", type=("build", "run"))
    depends_on("r-lme4@1.0:", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
