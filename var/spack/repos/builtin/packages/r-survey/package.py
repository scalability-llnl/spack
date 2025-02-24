# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSurvey(RPackage):
    """Analysis of Complex Survey Samples.

    Summary statistics, two-sample tests, rank tests, generalised linear
    models, cumulative link models, Cox models, loglinear models, and general
    maximum pseudolikelihood estimation for multistage stratified,
    cluster-sampled, unequally weighted survey samples. Variances by Taylor
    series linearisation or replicate weights. Post-stratification,
    calibration, and raking. Two-phase subsampling designs. Graphics. PPS
    sampling without replacement. Principal components, factor analysis."""

    cran = "survey"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("4.4-2", sha256="8a4a0f3122f0971f7c8756805add781192c655f507b235801dd78457a8d2f1bd")
    version("4.1-1", sha256="05e89a1678a39e32bfb41af8a31d643b04fc4d2660a96e701825e6bffcd75a52")
    version("4.0", sha256="b053f40f4cfa90507ca524f72d3b3a4b4869def52f11f907a14f1c6d90063de1")
    version("3.36", sha256="90f32e9d2b52eacf881e6717a4b5edfc5a3beb5da516f8372293549589d79475")
    version("3.35-1", sha256="11e5ddde9c8c21dfaed0b1247036e068ad32782c76ff71f7937eb7585dd364db")
    version("3.30-3", sha256="be45d00b22d857e66905789031f2db1037505f80ce15d4b0ea84dabb03bc9e6d")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r@2.16.0:", type=("build", "run"), when="@3.32:")
    depends_on("r@3.1.0:", type=("build", "run"), when="@3.35:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@4.1-1:")
    depends_on("r@4.1.0:", type=("build", "run"), when="@4.4-2:")
    depends_on("r-matrix", type=("build", "run"), when="@3.31:")
    depends_on("r-survival", type=("build", "run"), when="@3.31:")
    depends_on("r-lattice", type=("build", "run"), when="@3.31:")
    depends_on("r-minqa", type=("build", "run"), when="@3.34:")
    depends_on("r-numderiv", type=("build", "run"), when="@3.34:")
    depends_on("r-mitools@2.4:", type=("build", "run"), when="@3.36:")
    depends_on("r-rcpp@0.12.8:", type=("build", "run"), when="@4.4:")
    depends_on("r-rcpparmadillo", type=("build", "run"), when="@4.4:")
