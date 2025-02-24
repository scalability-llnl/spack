# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHh(RPackage):
    """Statistical Analysis and Data Display: Heiberger and Holland.

    Support software for Statistical Analysis and Data Display (Second Edition,
    Springer, ISBN 978-1-4939-2121-8, 2015) and (First Edition, Springer, ISBN
    0-387-40270-5, 2004) by Richard M. Heiberger and Burt Holland. This
    contemporary presentation of statistical methods features extensive use of
    graphical displays for exploring data and for displaying the analysis. The
    second edition includes redesigned graphics and additional chapters. The
    authors emphasize how to construct and interpret graphs, discuss principles
    of graphical design, and show how accompanying traditional tabular results
    are used to confirm the visual impressions derived directly from the
    graphs. Many of the graphical formats are novel and appear here for the
    first time in print. All chapters have exercises.  All functions introduced
    in the book are in the package. R code for all examples, both graphs and
    tables, in the book is included in the scripts directory of the package."""

    cran = "HH"

    version("3.1-52", sha256="d5495e18df65de613d9bdc43729ca2ac27746b15b90c06502b2ee5e2458d0383")
    version("3.1-49", sha256="12cef0cb0a07c745026d925aee2970913e1f3f0705a58bc2741bf4940c80b87b")
    version("3.1-47", sha256="50910ac7de49122df56c6e42413535601c74bbef9240ad8977e3267273d087c0")
    version("3.1-43", sha256="2ed35c8fc97092e9d2ce3439a2ec342d5d7bd93ad8f5266995cc80d88cd2235b")
    version("3.1-40", sha256="795924d900a98ae367e6697b2c951c3b4910a54931aebcad5024eda083d4a8a2")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-latticeextra", type=("build", "run"))
    depends_on("r-multcomp", type=("build", "run"))
    depends_on("r-gridextra@2.0.0:", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-leaps", type=("build", "run"))
    depends_on("r-vcd", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-shiny@0.13.1:", type=("build", "run"))
    depends_on("r-hmisc", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-rmpfr@0.6.0:", type=("build", "run"))
