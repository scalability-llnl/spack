# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStabledist(RPackage):
    """Stable Distribution Functions.

    Density, Probability and Quantile functions, and random number generation
    for (skew) stable distributions, using the parametrizations of Nolan."""

    cran = "stabledist"

    license("GPL-2.0-or-later")

    version("0.7-2", sha256="26671710c0d8e3c815b56e6e4f6bc9ea0509db47c0ef5b8acfbfa16095a16fd5")
    version("0.7-1", sha256="06c5704d3a3c179fa389675c537c39a006867bc6e4f23dd7e406476ed2c88a69")

    depends_on("r@3.1.0:", type=("build", "run"))
