# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMulttest(RPackage):
    """Resampling-based multiple hypothesis testing.

    Non-parametric bootstrap and permutation resampling-based multiple
    testing procedures (including empirical Bayes methods) for controlling
    the family-wise error rate (FWER), generalized family-wise error rate
    (gFWER), tail probability of the proportion of false positives (TPPFP),
    and false discovery rate (FDR). Several choices of bootstrap-based null
    distribution are implemented (centered, centered and scaled, quantile-
    transformed). Single-step and step-wise methods are available. Tests
    based on a variety of t- and F-statistics (including t-statistics based
    on regression parameters from linear and survival models as well as
    those based on correlation parameters) are included. When probing
    hypotheses with t-statistics, users may also select a potentially faster
    null distribution which is multivariate normal with mean zero and
    variance covariance matrix derived from the vector influence function.
    Results are reported in terms of adjusted p-values, confidence regions
    and test statistic cutoffs. The procedures are directly applicable to
    identifying differentially expressed genes in DNA microarray
    experiments."""

    bioc = "multtest"

    version("2.56.0", commit="619975704a271cdb74d97a75bee7e2df0028b4d3")
    version("2.54.0", commit="4e2c9e939dfd9984d8ff4bab0a95e1bd0457ec72")
    version("2.52.0", commit="00cfc9beb6d063c2b04fc83495a76824f8a33a64")
    version("2.50.0", commit="1de96649a942b115d3d554394514745e86eb3fd3")
    version("2.46.0", commit="c4dd27b333c80313a88668b59d0299988c6478a2")
    version("2.40.0", commit="5f00017c2d3a31e05e1cfe06d9f7afdee19f8473")
    version("2.38.0", commit="4dfe71cecfb298a94521088fb7bd83c5498d2915")
    version("2.36.0", commit="babb15e8d110eb72300ad59cf7e53386237a4198")
    version("2.34.0", commit="6ef873e05e6c93ede54f3421424f56eda057cd54")
    version("2.32.0", commit="c5e890dfbffcc3a3f107303a24b6085614312f4a")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
