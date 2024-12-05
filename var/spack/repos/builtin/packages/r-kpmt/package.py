# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKpmt(RPackage):
    """Known Population Median Test.

    Functions that implement the known population median test."""

    cran = "kpmt"

    license("MIT")

    version("0.1.0", sha256="6342ad02c93bfa7a764d028821bb6115bb8bc8c55b057a5860736cc0e034a295")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
