# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStargazer(RPackage):
    """Well-Formatted Regression and Summary Statistics Tables.

    Produces LaTeX code, HTML/CSS code and ASCII text for well-formatted tables
    that hold regression analysis results from several models side-by-side, as
    well as summary statistics."""

    cran = "stargazer"

    license("GPL-2.0-or-later")

    version("5.2.3", sha256="208e9b48a11cf56ce142731c204f3d2bcb5b68719f84309a36362cd925414265")
    version("5.2.2", sha256="70eb4a13a6ac1bfb35af07cb8a63d501ad38dfd9817fc3fba6724260b23932de")
