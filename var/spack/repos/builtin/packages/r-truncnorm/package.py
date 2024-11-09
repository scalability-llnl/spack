# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTruncnorm(RPackage):
    """Truncated Normal Distribution.

    Density, probability, quantile and random number generation functions for
    the truncated normal distribution."""

    cran = "truncnorm"

    license("GPL-2.0-or-later")

    version("1.0-9", sha256="5156acc4d63243bf95326d6285b0ba3cdf710697d67c233a12ae56f3d87ec708")
    version("1.0-8", sha256="49564e8d87063cf9610201fbc833859ed01935cc0581b9e21c42a0d21a47c87e")
    version("1.0.0", sha256="dc1b018cb6d9ad5beb2d9e2f3ebe56c3f69d7a98fc5a1d963dd7933d209ac272")

    depends_on("c", type="build")  # generated

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0-8:")
