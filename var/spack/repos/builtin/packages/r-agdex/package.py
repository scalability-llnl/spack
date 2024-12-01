# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAgdex(RPackage):
    """Agreement of Differential Expression Analysis.

    A tool to evaluate agreement of differential expression for cross-
    species genomics"""

    bioc = "AGDEX"

    version("1.48.0", commit="917920b397493b0ea40093044ebe36fff7c389ad")
    version("1.46.0", commit="d7c38e8bdcaa7b0261117c605e7f61e2b07e8316")
    version("1.44.0", commit="9d3eb90eaf7bf093c7fa73facb3df89506a85185")
    version("1.42.0", commit="175cf1b384b0942103d841b1feb9e4f7d141ba06")
    version("1.38.0", commit="7e2c1f5f27ccbea6a7157f5122212e40408b74da")
    version("1.32.0", commit="254ad2c876ab9ac48c3c3b395160dccabc084acf")
    version("1.30.0", commit="d6cc21ed7e11e6644399495fa5f8b36368625d4b")
    version("1.28.0", commit="7d78ee424485018b73cd019ceaed7a2ed53adf3f")
    version("1.26.0", commit="260bc641111770176707d4d43e67b5877bf5eb82")
    version("1.24.0", commit="29c6bcfa6919a5c6d8bcb36b44e75145a60ce7b5")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-gseabase", type=("build", "run"))
