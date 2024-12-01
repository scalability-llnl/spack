# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSinglecellexperiment(RPackage):
    """S4 Classes for Single Cell Data.

    Defines a S4 class for storing data from single-cell experiments. This
    includes specialized methods to store and retrieve spike-in information,
    dimensionality reduction coordinates and size factors for each cell,
    along with the usual metadata for genes and libraries."""

    bioc = "SingleCellExperiment"

    version("1.22.0", commit="d477e8ef442dec60576e08bb660081b8bccc978c")
    version("1.20.0", commit="467f02c0346e3ca5ec8825a6faa80a90d20fcd29")
    version("1.18.1", commit="db7768a7cb5eca724bcf7e4cea3234992ac714a1")
    version("1.18.0", commit="3a72dcd97e628055b2d02294eaecca9a41aba604")
    version("1.16.0", commit="bb27609ba08052607fc08529ffbbbcf1eab265cb")
    version("1.12.0", commit="66063b74c8b0bd0fd1277c7ad425ad11823ab356")
    version("1.6.0", commit="baa51d77a8dacd2a22e7293095a8cffaaa3293b4")
    version("1.4.1", commit="b1efcb338e9176ae6829bb897957aa37e74d4870")
    version("1.2.0", commit="fe512259da79e0c660b322b5387e9bb16f2e6321")
    version("1.0.0", commit="545e974aa7ca7855e039bf9e3030290cd71d9031")

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.2.0:1.6.0")
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"), when="@1.16.0:")
    depends_on("r-delayedarray", type=("build", "run"), when="@1.16.0:")
