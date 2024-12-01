# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyexpress(RPackage):
    """Affymetrix Quality Assessment and Analysis Tool.

    The purpose of this package is to provide a comprehensive and easy-to-
    use tool for quality assessment and to identify differentially expressed
    genes in the Affymetrix gene expression data."""

    bioc = "AffyExpress"

    version("1.56.0", commit="e07085833de2bbf81537410cad526d39f8a82478")
    version("1.50.0", commit="8b98703b63396df9692afb0e15b594658125cc96")
    version("1.48.0", commit="dbaed516b7529ef4f7588aafaf3c5f1d53a9bb92")
    version("1.46.0", commit="2add4a4436e21aa20f1ededbfd5f1365a3d28c85")
    version("1.44.0", commit="7517bc8b363ceb107d5dca66dd74f94edefde52a")
    version("1.42.0", commit="f5c5cf6173f4419e25f4aeff5e6b705a40abc371")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-affy@1.23.4:", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
