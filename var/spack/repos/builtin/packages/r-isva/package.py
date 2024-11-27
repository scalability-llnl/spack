# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIsva(RPackage):
    """Independent Surrogate Variable Analysis.

    Independent Surrogate Variable Analysis is an algorithm for feature
    selection in the presence of potential confounding factors (see
    Teschendorff AE et al 2011, <doi:10.1093/bioinformatics/btr171>)."""

    cran = "isva"

    license("GPL-2.0-only")

    version("1.9", sha256="9fd016e0b34034d271d45f8a0d0db62780bf0187112e45f610aa9237014e1d17")

    depends_on("r-qvalue", type=("build", "run"))
    depends_on("r-fastica", type=("build", "run"))
    depends_on("r-jade", type=("build", "run"))
