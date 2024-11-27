# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamm4(RPackage):
    """Generalized Additive Mixed Models using 'mgcv' and 'lme4'.

    Estimate generalized additive mixed models via a version of function gamm()
    from 'mgcv', using 'lme4' for estimation."""

    cran = "gamm4"

    license("GPL-2.0-or-later")

    version("0.2-6", sha256="57c5b66582b2adc32f6a3bb6a259f5b95198e283a96d966a6007e8e48b380c89")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-lme4@1.0:", type=("build", "run"))
    depends_on("r-mgcv@1.7-23:", type=("build", "run"))
