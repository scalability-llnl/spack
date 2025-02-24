# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRfast(RPackage):
    """A Collection of Efficient and Extremely Fast R Functions.

    A collection of fast (utility) functions for data analysis. Column- and
    row- wise means, medians, variances, minimums, maximums, many t, F and
    G-square tests, many regressions (normal, logistic, Poisson), are some of
    the many fast functions. References: a) Tsagris M., Papadakis M. (2018).
    Taking R to its limits: 70+ tips. PeerJ Preprints 6:e26605v1
    <doi:10.7287/peerj.preprints.26605v1>. b) Tsagris M. and Papadakis M.
    (2018). Forward regression in R: from the extreme slow to the extreme fast.
    Journal of Data Science, 16(4): 771-780.
    <doi:10.6339/JDS.201810_16(4).00006>."""

    cran = "Rfast"

    version("2.1.0", sha256="f9e46cac99db756cd49c9cd83be8adc0d381e6c03102389bfdcb8258d02418ff")
    version("2.0.7", sha256="8f86159a4760a7124e1c91ae0b022c7e496f81590ea4e4af702bea44e8dedf8f")
    version("2.0.6", sha256="34694b5c67ce8fcbdc90aac2ac80a74d4b66515f383e6301aea7c020009ebe7f")
    version("2.0.4", sha256="959907e36e24620c07ec282b203b40214f4914f4928c07ee6491043c27af31d9")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.3:", type=("build", "run"))
    depends_on("r-rcppparallel", type=("build", "run"), when="@2.1.0:")
    depends_on("r-rcppziggurat", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
