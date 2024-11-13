# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRuv(RPackage):
    """Detect and Remove Unwanted Variation using Negative Controls.

    Implements the 'RUV' (Remove Unwanted Variation) algorithms. These
    algorithms attempt to adjust for systematic errors of unknown origin in
    high-dimensional data. The algorithms were originally developed for use
    with genomic data, especially microarray data, but may be useful with other
    types of high-dimensional data as well. These algorithms were proposed in
    Gagnon-Bartsch and Speed (2012) <doi:10.1093/nar/gkz433>, Gagnon-Bartsch,
    Jacob and Speed (2013), and Molania, et. al. (2019)
    <doi:10.1093/nar/gkz433>. The algorithms require the user to specify a set
    of negative control variables, as described in the references. The
    algorithms included in this package are 'RUV-2', 'RUV-4', 'RUV-inv',
    'RUV-rinv', 'RUV-I', and RUV-III', along with various supporting
    algorithms."""

    cran = "ruv"

    license("GPL-2.0-or-later")

    version("0.9.7.1", sha256="a0c54e56ba3d8f6ae178ae4d0e417a79295abf5dcb68bbae26c4b874734d98d8")

    depends_on("c", type="build")  # generated

    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
