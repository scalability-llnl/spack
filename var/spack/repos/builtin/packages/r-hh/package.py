# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHh(RPackage):
    """HH: Statistical Analysis and Data Display: Heiberger and Holland.

    Support software for Statistical Analysis and Data Display (Second
    Edition, Springer, ISBN 978-1-4939-2121-8, 2015) and (First Edition,
    Springer, ISBN 0-387-40270-5, 2004) by Richard M. Heiberger and Burt
    Holland. This contemporary presentation of statistical methods features
    extensive use of graphical displays for exploring data and for displaying
    the analysis. The second edition includes redesigned graphics and
    additional chapters. The authors emphasize how to construct and interpret
    graphs, discuss principles of graphical design, and show how accompanying
    traditional tabular results are used to confirm the visual impressions
    derived directly from the graphs. Many of the graphical formats are novel
    and appear here for the first time in print. All chapters have exercises.
    All functions introduced in the book are in the package. R code for all
    examples, both graphs and tables, in the book is included in the scripts
    directory of the package."""

    homepage = "https://cloud.r-project.org/package=HH"
    url      = "https://cloud.r-project.org/src/contrib/HH_3.1-40.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/HH"

    version('3.1-40', sha256='795924d900a98ae367e6697b2c951c3b4910a54931aebcad5024eda083d4a8a2')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-latticeextra', type=('build', 'run'))
    depends_on('r-multcomp', type=('build', 'run'))
    depends_on('r-gridextra@2.0.0:', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-leaps', type=('build', 'run'))
    depends_on('r-vcd', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-shiny@0.13.1:', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-abind', type=('build', 'run'))
    depends_on('r-rmpfr@0.6.0:', type=('build', 'run'))
