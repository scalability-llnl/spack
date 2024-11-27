# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCorpcor(RPackage):
    """Efficient Estimation of Covariance and (Partial) Correlation.

    Implements a James-Stein-type shrinkage estimator for  the covariance
    matrix, with separate shrinkage for variances and correlations.   The
    details of the method are explained in Schafer and Strimmer (2005)
    <DOI:10.2202/1544-6115.1175> and Opgen-Rhein and Strimmer (2007)
    <DOI:10.2202/1544-6115.1252>.  The approach is both computationally as well
    as statistically very efficient, it is applicable to "small n, large p"
    data,  and always returns a positive definite and well-conditioned
    covariance matrix.   In addition to inferring the covariance matrix the
    package also provides  shrinkage estimators for partial correlations and
    partial variances.   The inverse of the covariance and correlation matrix
    can be efficiently computed, as well as any arbitrary power of the
    shrinkage correlation matrix.  Furthermore, functions are available for
    fast  singular value decomposition, for computing the pseudoinverse, and
    for  checking the rank and positive definiteness of a matrix."""

    cran = "corpcor"

    license("GPL-3.0-or-later")

    version("1.6.10", sha256="71a04c503c93ec95ddde09abe8c7ddeb36175b7da76365a14b27066383e10e09")
    version("1.6.9", sha256="2e4fabd1d3936fecea67fa365233590147ca50bb45cf80efb53a10345a8a23c2")

    depends_on("r@3.0.2:", type=("build", "run"))
