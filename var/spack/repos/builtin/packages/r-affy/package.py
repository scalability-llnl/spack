# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffy(RPackage):
    """Methods for Affymetrix Oligonucleotide Arrays.

    The package contains functions for exploratory oligonucleotide array
    analysis. The dependence on tkWidgets only concerns few convenience
    functions. 'affy' is fully functional without it."""

    bioc = "affy"

    version("1.78.0", commit="cc7eac358b6e10ee86a7a93d2e436758f6fbd9b5")
    version("1.76.0", commit="3bb309388d5d6402c356d4a5270ee83c5b88942f")
    version("1.74.0", commit="2266c4a46eda7e5b64f7f3e17e8b61e7b85579ff")
    version("1.72.0", commit="3750b4eb8e5224b19100f6c881b67e568d8968a2")
    version("1.68.0", commit="1664399610c9aa519399445a2ef8bb9ea2233eac")
    version("1.62.0", commit="097ab4aa98a1700c5fae65d07bed44a477714605")
    version("1.60.0", commit="fcae363e58b322ad53584d9e15e80fa2f9d17206")
    version("1.58.0", commit="4698231f45f225228f56c0708cd477ad450b4ee6")
    version("1.56.0", commit="d36a7b8f05b1ef60162d94e75037d45c48f88871")
    version("1.54.0", commit="a815f02906fcf491b28ed0a356d6fce95a6bd20e")

    depends_on("c", type="build")  # generated

    depends_on("r@2.8.0:4.0", type=("build", "run"), when="@:1.68.0")
    depends_on("r-biocgenerics@0.1.12:", type=("build", "run"))
    depends_on("r-biobase@2.5.5:", type=("build", "run"))
    depends_on("r-affyio@1.13.3:", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@1.60.0:")
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-zlibbioc", type=("build", "run"))

    depends_on("r-biocinstaller", type=("build", "run"), when="@1.54.0:1.58.0")
