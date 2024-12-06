# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsolnp(RPackage):
    """General Non-Linear Optimization.

    General Non-linear Optimization Using Augmented Lagrange Multiplier
    Method."""

    cran = "Rsolnp"

    version("1.16", sha256="3142776062beb8e2b45cdbc4fe6e5446b6d33505253d79f2890fe4178d9cf670")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-truncnorm", type=("build", "run"))
