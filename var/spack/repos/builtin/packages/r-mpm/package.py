# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMpm(RPackage):
    """Multivariate Projection Methods.

    Exploratory graphical analysis of multivariate data, specifically gene
    expression data with different projection methods: principal component
    analysis, correspondence analysis, spectral map analysis."""

    cran = "mpm"

    license("GPL-2.0-or-later")

    version("1.0-23", sha256="d2abda28246842b187b796a730c6e0590182960fda3bbf16ce4a1d5e5b13fbca")
    version("1.0-22", sha256="d3ba4053cd57a189cb65c5fa20e6a4152374aead8c985254cb6e550e36e23272")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
