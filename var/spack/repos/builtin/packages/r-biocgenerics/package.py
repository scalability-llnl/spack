# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocgenerics(RPackage):
    """S4 generic functions used in Bioconductor.

    The package defines S4 generic functions used in Bioconductor."""

    bioc = "BiocGenerics"

    version("0.46.0", commit="a90f0c5976a24417e47e009ba602fc98515ac9ab")
    version("0.44.0", commit="d7cd9c19958bd8d4573d980494188fa15ab16e45")
    version("0.42.0", commit="3582d47b836387afc08157f3d6a5013fd64334ed")
    version("0.40.0", commit="0bc1e0ed4d20c7101cd782a14f6373e27478acfc")
    version("0.36.0", commit="0d5d169d7d64d648a22f9043837c93bc784e71ed")
    version("0.34.0", commit="f7c2020b6fb06ade6d70b4de17672735edfa45df")
    version("0.30.0", commit="fc7c3af4a5635a30988a062ed09332c13ca1d1a8")
    version("0.28.0", commit="041fc496504f2ab1d4d863fffb23372db214394b")
    version("0.26.0", commit="5b2a6df639e48c3cd53789e0b174aec9dda6b67d")
    version("0.24.0", commit="3db111e8c1f876267da89f4f0c5406a9d5c31cd1")
    version("0.22.1", commit="9c90bb8926885289d596a81ff318ee3745cbb6ad")

    depends_on("r@3.6.0:", type=("build", "run"), when="@0.30.0:")
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.36.0:")
