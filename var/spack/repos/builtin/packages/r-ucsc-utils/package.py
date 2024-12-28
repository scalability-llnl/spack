# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUcscUtils(RPackage):
    """Low-level utilities to retrieve data from the UCSC Genome Browser."""

    bioc = "UCSC.utils"

    version("1.2.0", commit="d77d73e9064aafc9aba1fdeed73233a68f8c61db")
    version("1.0.0", commit="dc5a0a84eaab8a0f20f136a6802de583a0c15c1a")

    depends_on("r-httr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
