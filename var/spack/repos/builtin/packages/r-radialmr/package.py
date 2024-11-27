# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRadialmr(RPackage):
    """RadialMR.

    A package for implementing radial inverse variance weighted and MR-Egger
    methods."""

    homepage = "https://github.com/WSpiller/RadialMR"
    git = "https://github.com/WSpiller/RadialMR"

    license("GPL-3.0-or-later")

    version("1.0", commit="d63d3fc8270836ab441b9e14a5ba3eeb2795d7cb")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-plotly", type=("build", "run"))
