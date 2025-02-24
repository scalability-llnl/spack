# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatExplore(RPackage):
    """Exploratory Data Analysis for the 'spatstat' Family.

    Functionality for exploratory data analysis and nonparametric analysis of
    spatial data, mainly spatial point patterns, in the 'spatstat' family of
    packages. (Excludes analysis of spatial data on a linear network, which is
    covered by the separate package 'spatstat.linnet'.) Methods include quadrat
    counts, K-functions and their simulation envelopes, nearest neighbour
    distance and empty space statistics, Fry plots, pair correlation function,
    kernel smoothed intensity, relative risk estimation with cross-validated
    bandwidth selection, mark correlation functions, segregation indices, mark
    dependence diagnostics, and kernel estimates of covariate effects. Formal
    hypothesis tests of random pattern (chi-squared, Kolmogorov-Smirnov, Monte
    Carlo, Diggle-Cressie-Loosmore-Ford, Dao-Genton, two-stage Monte Carlo) and
    tests for covariate effects (Cox-Berman-Waller-Lawson, Kolmogorov-Smirnov,
    ANOVA) are also supported."""

    cran = "spatstat.explore"

    version("3.3-2", sha256="a24827d24a86f2f20f8dcbbb5f57f5ab43345fa346c572099b84d867e7bf85ed")
    version("3.1-0", sha256="87ef4882652db3b834214bfc776dd7d23d931a9227de12f19722aeb1029d086e")
    version("3.0-3", sha256="137444a46d26d88241336feece63ed7b006a9328cfe3861d4b8ab7b4bed963a7")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-spatstat-data@3.0:", type=("build", "run"))
    depends_on("r-spatstat-data@3.0-4:", type=("build", "run"), when="@:")
    depends_on("r-spatstat-data@3.1-2:", type=("build", "run"), when="@3.3-2:")
    depends_on("r-spatstat-geom@3.0:", type=("build", "run"))
    depends_on("r-spatstat-geom@3.0-5:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-geom@3.2-9:", type=("build", "run"), when="@:")
    depends_on("r-spatstat-geom@3.3-2:", type=("build", "run"), when="@3.3-2:")
    depends_on("r-spatstat-random@3.0:", type=("build", "run"))
    depends_on("r-spatstat-random@3.1:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-random@3.3-1:", type=("build", "run"), when="@3.3-2:")
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-spatstat-univar@3.0-0:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-spatstat-utils@3.0:", type=("build", "run"))
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-utils@3.1-0:", type=("build", "run"), when="@3.3-2:")
    depends_on("r-spatstat-sparse@3.0:", type=("build", "run"))
    depends_on("r-spatstat-sparse@3.1-0:", type=("build", "run"), when="@3.3-2:")
    depends_on("r-goftest@1.2-2:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
