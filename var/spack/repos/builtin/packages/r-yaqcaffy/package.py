# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYaqcaffy(RPackage):
    """Affymetrix expression data quality control and reproducibility analysis.

    Quality control of Affymetrix GeneChip expression data and
    reproducibility analysis of human whole genome chips with the MAQC
    reference datasets."""

    bioc = "yaqcaffy"

    version("1.50.0", commit="b32e6b947ca9c4ab7163cfddc084a1bc0a34780e")
    version("1.44.0", commit="00898f3ec9ac0beadbcf57bda3d3c1c99fb0c3c0")
    version("1.42.0", commit="a4af673774165e087499ecc35f96aab6bbfbeea1")
    version("1.40.0", commit="0c78f8ff8f675305f6fa4b052d2482e9aee551bb")
    version("1.38.0", commit="d57100862c2dc0f5e7684f318b9ceda7349352be")
    version("1.36.0", commit="4d46fe77b2c8de2230a77b0c07dd5dd726e3abd6")

    depends_on("r-simpleaffy@2.19.3:", type=("build", "run"))
