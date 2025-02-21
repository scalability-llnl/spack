# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMultcompview(RPackage):
    """Visualizations of Paired Comparisons.

    Convert a logical vector or a vector of p-values or a correlation,
    difference, or distance matrix into a display identifying the pairs for
    which the differences were not significantly different. Designed for use in
    conjunction with the output of functions like TukeyHSD, dist{stats},
    simint, simtest, csimint, csimtest{multcomp}, friedmanmc,
    kruskalmc{pgirmess}."""

    cran = "multcompView"

    version("0.1-10", sha256="38f249b22758c9f727b1656d1a08c6022a06a1ea319364ff680147d64598ad8a")
    version("0.1-9", sha256="1f3993e9d51f3c7a711a881b6a20081a85ffab60c27828ceb3640a6b4c887397")
    version("0.1-8", sha256="123d539172ad6fc63d83d1fc7f356a5ed7b691e7803827480118bebc374fd8e5")
