# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAcepack(RPackage):
    """ACE and AVAS for Selecting Multiple Regression Transformations.

    Two nonparametric methods for multiple regression transform selection are
    provided. The first, Alternative Conditional Expectations (ACE), is an
    algorithm to find the fixed point of maximal correlation, i.e. it finds a
    set of transformed response variables that maximizes R^2 using smoothing
    functions [see Breiman, L., and J.H. Friedman. 1985. "Estimating Optimal
    Transformations for Multiple Regression and Correlation". Journal of the
    American Statistical Association. 80:580-598.
    <doi:10.1080/01621459.1985.10478157>]. Also included is the Additivity
    Variance Stabilization (AVAS) method which works better than ACE when
    correlation is low [see Tibshirani, R.. 1986. "Estimating Transformations
    for Regression via Additivity and Variance Stabilization". Journal of the
    American Statistical Association. 83:394-405.
    <doi:10.1080/01621459.1988.10478610>]. A good introduction to these two
    methods is in chapter 16 of Frank Harrel's "Regression Modeling Strategies"
    in the Springer Series in Statistics."""

    cran = "acepack"

    license("MIT")

    version("1.4.2", sha256="5bffcd12b783f372bb6c50e35317744ac31597c91b6433442a7b0dce2f66ac91")
    version("1.4.1", sha256="82750507926f02a696f6cc03693e8d4a5ee7e92500c8c15a16a9c12addcd28b9")
