# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAde4(RPackage):
    """Analysis of Ecological Data : Exploratory and Euclidean Methods in
    Environmental Sciences.

    Tools for multivariate data analysis. Several methods are provided for the
    analysis (i.e., ordination) of one-table (e.g., principal component
    analysis, correspondence analysis), two-table (e.g., coinertia analysis,
    redundancy analysis), three-table (e.g., RLQ analysis) and K-table (e.g.,
    STATIS, multiple coinertia analysis). The philosophy of the package is
    described in Dray and Dufour (2007) <doi:10.18637/jss.v022.i04>."""

    cran = "ade4"

    license("GPL-2.0-or-later")

    version("1.7-22", sha256="007df54e83a2a6cb8d6da8006f0aace011e7eaa7744dc5f8230ac2c002b393b4")
    version("1.7-20", sha256="ddc75788b55902f17dabda209eb67c378aa0233767697e00fa3f8fc85e4bad7b")
    version("1.7-19", sha256="c85111881ff93a261ca34a5b5ef313d1c0ff9b84f0b23596bc56cfa696f165ef")
    version("1.7-18", sha256="ecb6f4c42c60f39702aa96f454bb536a333049c9608ee2b6bdf8795e059cc525")
    version("1.7-16", sha256="9bd7a25ff4fe30a32fd8f6b71909f4c638a0e2f002fc8303c0a4795423385590")
    version("1.7-13", sha256="f5d0a7356ae63f82d3adb481a39007e7b0d70211b8724aa686af0c89c994e99b")
    version("1.7-11", sha256="4ccd799ae99bd625840b866a697c4a48adb751660470bf0d6cf9207b1927a572")
    version("1.7-6", sha256="80848e1650dcc0ec921c130efa6f7e9b307f0d107c63e49faa52296eda19cc52")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-pixmap", type=("build", "run"), when="@1.7-16:")
    depends_on("r-sp", type=("build", "run"), when="@1.7-16:")
    depends_on("r-rcpp", type=("build", "run"), when="@1.7-22:")
    depends_on("r-rcpparmadillo", type=("build", "run"), when="@1.7-22:")

    depends_on("r-progress", type=("build", "run"), when="@1.7-16")
