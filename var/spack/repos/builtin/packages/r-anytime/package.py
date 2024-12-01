# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnytime(RPackage):
    """Anything to 'POSIXct' or 'Date' Converter.

    Convert input in any one of character, integer, numeric, factor, or ordered
    type into 'POSIXct' (or 'Date') objects, using one of a number of
    predefined formats, and relying on Boost facilities for date and time
    parsing."""

    cran = "anytime"

    license("GPL-2.0-or-later")

    version("0.3.9", sha256="1096c15249ac70997a8a41c37eeb2a6d38530621abeae05d3dcd96a8acc7574a")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.9:", type=("build", "run"))
    depends_on("r-bh", type=("build", "run"))
