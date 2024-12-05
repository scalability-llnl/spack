# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJaspar2018(RPackage):
    """Data package for JASPAR 2018.

    Data package for JASPAR 2018. To search this databases, please use the
    package TFBSTools (>= 1.15.6)."""

    bioc = "JASPAR2018"

    version("1.1.0", commit="cf8598d3c9054d85c43655cf82be17f74d800fa5")
    version("1.0.0", commit="4c84092b3737bb1c57ab56f4321f2f5e4b0efeaa")

    depends_on("r@3.4.0:", type=("build", "run"))
