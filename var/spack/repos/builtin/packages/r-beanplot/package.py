# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBeanplot(RPackage):
    """Visualization via Beanplots (like Boxplot/Stripchart/Violin Plot).

    Plots univariate comparison graphs, an alternative to
    boxplot/stripchart/violin plot."""

    cran = "beanplot"

    license("GPL-2.0-only")

    version("1.3.1", sha256="49158aee3449108fd857ef43fb777f55a2b975b350a4a710788996ad19dd15ad")
    version("1.2", sha256="49da299139a47171c5b4ccdea79ffbbc152894e05d552e676f135147c0c9b372")
