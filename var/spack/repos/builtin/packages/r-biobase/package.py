# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiobase(RPackage):
    """Biobase: Base functions for Bioconductor.

    Functions that are needed by many other packages or which replace R
    functions."""

    bioc = "Biobase"

    version("2.60.0", commit="8dc10d2d26dc0847740ff2b4f16cc1ae2e936464")
    version("2.58.0", commit="767f2f33f158f233616178e12ce08cdb03d2a5a2")
    version("2.56.0", commit="3b2dd91b333677c2f27257c7624014a55e73c52b")
    version("2.54.0", commit="8215d76ce44899e6d10fe8a2f503821a94ef6b40")
    version("2.50.0", commit="9927f90d0676382f2f99e099d8d2c8e2e6f1b4de")
    version("2.44.0", commit="bde2077f66047986297ec35a688751cdce150dd3")
    version("2.42.0", commit="3e5bd466b99e3cc4af1b0c3b32687fa56d6f8e4d")
    version("2.40.0", commit="6555edbbcb8a04185ef402bfdea7ed8ac72513a5")
    version("2.38.0", commit="83f89829e0278ac014b0bc6664e621ac147ba424")
    version("2.36.2", commit="15f50912f3fa08ccb15c33b7baebe6b8a59ce075")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biocgenerics@0.3.2:", type=("build", "run"))
    depends_on("r-biocgenerics@0.27.1:", type=("build", "run"), when="@2.42.0:")
