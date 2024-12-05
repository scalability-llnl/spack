# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMutoss(RPackage):
    """Unified Multiple Testing Procedures.

    Designed to ease the application and comparison of multiple hypothesis
    testing procedures for FWER, gFWER, FDR and FDX. Methods are standardized
    and usable by the accompanying 'mutossGUI'."""

    cran = "mutoss"

    license("GPL-2.0-or-later")

    version("0.1-13", sha256="b60f6fcdce44dc60c7d34c6510047f756f1442366a3566661b22aae12f4ff141")
    version("0.1-12", sha256="2889ae3d502157592697124eb86adc14911e2b7fdaa7204743a376b1eeb967fa")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))
    depends_on("r-plotrix", type=("build", "run"))
    depends_on("r-multtest@2.2.0:", type=("build", "run"))
    depends_on("r-multcomp@1.1-0:", type=("build", "run"))
