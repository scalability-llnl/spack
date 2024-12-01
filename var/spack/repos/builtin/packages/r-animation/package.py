# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnimation(RPackage):
    """A Gallery of Animations in Statistics and Utilities to Create
    Animations.

    Provides functions for animations in statistics, covering topics in
    probability theory, mathematical statistics, multivariate statistics,
    non-parametric statistics, sampling survey, linear models, time series,
    computational statistics, data mining and machine learning.  These
    functions maybe helpful in teaching statistics and data analysis."""

    cran = "animation"

    license("GPL-2.0-or-later")

    version("2.7", sha256="88418f1b04ec785963bad492f30eb48b05914e9e5d88c7eef705d949cbd7e469")
    version("2.6", sha256="90293638920ac436e7e4de76ebfd92e1643ccdb0259b62128f16dd0b13245b0a")
    version("2.5", sha256="b232fef1b318c79710e5e1923d87baba4c85ffe2c77ddb188130e0911d8cb55f")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r-magick", type=("build", "run"), when="@2.6:")
    depends_on("imagemagick")
    depends_on("texlive@2019:")
    depends_on("swftools")
    depends_on("ffmpeg")
