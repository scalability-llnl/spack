# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPermute(RPackage):
    """Functions for Generating Restricted Permutations of Data.

    A set of restricted permutation designs for freely exchangeable, line
    transects (time series), and spatial grid designs plus permutation of
    blocks (groups of samples) is provided. 'permute' also allows split-plot
    designs, in which the whole-plots or split-plots or both can be
    freely-exchangeable or one of the restricted designs. The 'permute' package
    is modelled after the permutation schemes of 'Canoco 3.1' (and later) by
    Cajo ter Braak."""

    cran = "permute"

    license("GPL-2.0-only")

    version("0.9-7", sha256="eff88ffb579aaeb994e9f8609b776b2d9d9d56bc2879ddf180e3a2ad19f48dc0")
    version("0.9-5", sha256="d2885384a07497e8df273689d6713fc7c57a7c161f6935f3572015e16ab94865")
    version("0.9-4", sha256="a541a5f5636ddd67fd856d3e11224f15bc068e96e23aabe3e607a7e7c2fc1cf1")

    depends_on("r@2.14.0:", type=("build", "run"))
