# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlmnet(RPackage):
    """Lasso and Elastic-Net Regularized Generalized Linear Models.

    Extremely efficient procedures for fitting the entire lasso or elastic-net
    regularization path for linear regression, logistic and multinomial
    regression models, Poisson regression and the Cox model. Two recent
    additions are the multiple-response Gaussian, and the grouped multinomial.
    The algorithm uses cyclical coordinate descent in a path-wise fashion, as
    described in the paper linked to via the URL below."""

    cran = "glmnet"

    license("GPL-2.0-only")

    version("4.1-8", sha256="1ddbe5ce07076d1bdf58b0202ebd0ceac8eeb4796c5175681adb9e58c30ddcfe")
    version("4.1-7", sha256="b3a0b606d99df0256eb68e6ebd271e071b246900a4379641af2e7d548c70eaa8")
    version("4.1-4", sha256="f6b0f70a0b3d81ff91c2b94f795a2a32e90dd458270f1a29e49e085dd65000f9")
    version("4.1-3", sha256="64bc35aa40b6e580cfb8a21e649eb103e996e8747a10c476b8bb9545c846325a")
    version("4.1", sha256="8f0af50919f488789ecf261f6e0907f367d89fca812baa2f814054fb2d0e40cb")
    version("2.0-18", sha256="e8dce9d7b8105f9cc18ba981d420de64a53b09abee219660d3612915d554256b")
    version("2.0-13", sha256="f3288dcaddb2f7014d42b755bede6563f73c17bc87f8292c2ef7776cb9b9b8fd")
    version("2.0-5", sha256="2ca95352c8fbd93aa7800f3d972ee6c1a5fcfeabc6be8c10deee0cb457fd77b1")

    depends_on("r@3.6.0:", type=("build", "run"), when="@4.1:")

    depends_on("r-matrix@1.0-6:", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-shape", type=("build", "run"), when="@4.1:")
    depends_on("r-survival", type=("build", "run"), when="@4.1:")
    depends_on("r-rcpp", type=("build", "run"), when="@4.1-3:")
    depends_on("r-rcppeigen", type=("build", "run"), when="@4.1-3:")
