# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPbivnorm(RPackage):
    """Vectorized Bivariate Normal CDF.

    Provides a vectorized R function for calculating probabilities from a
    standard bivariate normal CDF."""

    cran = "pbivnorm"

    license("GPL-2.0-or-later")

    version("0.6.0", sha256="07c37d507cb8f8d2d9ae51a9a6d44dfbebd8a53e93c242c4378eaddfb1cc5f16")

    depends_on("fortran", type="build")  # generated
