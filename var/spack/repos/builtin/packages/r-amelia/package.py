# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAmelia(RPackage):
    """A Program for Missing Data.

    A tool that "multiply imputes" missing data in a single cross-section (such
    as a survey), from a time series (like variables collected for each year in
    a country), or from a time-series-cross-sectional data set (such as
    collected by years for each of several countries). Amelia II implements our
    bootstrapping-based algorithm that gives essentially the same answers as
    the standard IP or EMis approaches, is usually considerably faster than
    existing approaches and can handle many more variables.  Unlike Amelia I
    and other statistically rigorous imputation software, it virtually never
    crashes (but please let us know if you find to the contrary!).  The program
    also generalizes existing approaches by allowing for trends in time series
    across observations within a cross-sectional unit, as well as priors that
    allow experts to incorporate beliefs they have about the values of missing
    cells in their data.  Amelia II also includes useful diagnostics of the fit
    of multiple imputation models.  The program works from the R command line
    or via a graphical user interface that does not require users to know R."""

    cran = "Amelia"

    version("1.8.2", sha256="4fb24a247ca20ba942e854f21e366fbbaf8fbcabc99efbb537511a10a732fc3e")
    version("1.8.1", sha256="120ce62a2acfc845dbeb155ce3f33b41ebad324bc73693a918a95194a9fc47e4")
    version("1.8.0", sha256="3ec1d5a68dac601b354227916aa8ec72fa1216b603dd887aae2b24cb69b5995e")
    version("1.7.6", sha256="63c08d374aaf78af46c34dc78da719b3085e58d9fabdc76c6460d5193a621bea")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-rcpp@0.11:", type=("build", "run"))
    depends_on("r-foreign", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.8.1:")
    depends_on("r-rcpparmadillo", type=("build", "run"))
