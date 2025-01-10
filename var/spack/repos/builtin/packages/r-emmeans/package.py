# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REmmeans(RPackage):
    """Estimated Marginal Means, aka Least-Squares Means.

    Obtain estimated marginal means (EMMs) for many linear, generalized linear,
    and mixed models. Compute contrasts or linear functions of EMMs, trends,
    and comparisons of slopes. Plots and other displays.  Least-squares means
    are discussed, and the term "estimated marginal means" is suggested, in
    Searle, Speed, and Milliken (1980) Population marginal means in the linear
    model: An alternative to least squares means, The American Statistician
    34(4), 216-221 <doi:10.1080/00031305.1980.10483031>."""

    cran = "emmeans"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("1.10.4", sha256="66653623c5984f99ba481a8611d6cf3b829e577f07bbe4043f279a3f8fbadcc3")
    version("1.8.5", sha256="5c88b415b5a42d8c1aa63af090c4987326530ea6d0e60bab9b5fb7e99a982415")
    version("1.8.2", sha256="785973457d8a6547df489f87b62987d44a68c4b9018661d38ca11ee34e49d209")
    version("1.8.1-1", sha256="79fc5e44255427b038d0dbe2c9887d84984baacb11bb9a9078cd8d0dca2e6577")
    version("1.7.4-1", sha256="f7a33a2b54ad13d6e39ee6c58004f83a9edb06e8dc8282180440610eb18be721")
    version("1.7.2", sha256="d3e51c2a4b6c74dd9840efebe241a53072172f269f4324421f28f68db71721bc")
    version("1.7.1-1", sha256="6b01eaad1ea0f96245db8563cc77929a3c3b96cd61c24ce1d452308d6e0250de")
    version("1.7.0", sha256="d4b654896197dfda8354b33257380a66ee06117d6177b1ed7f1e42176525e9c5")
    version("1.6.0", sha256="201bb7b008dde94231ed60bcc6a32749442faaab4baeea99ad28b97c951b3c1e")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@1.8.1-1:")
    depends_on("r-estimability@1.3:", type=("build", "run"))
    depends_on("r-estimability@1.4.1:", type=("build", "run"), when="@1.8.1-1:")
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-mvtnorm", type=("build", "run"))

    depends_on("r-plyr", type=("build", "run"), when="@:1.6")
    depends_on("r-xtable@1.8-2:", type=("build", "run"), when="@:1.8.2")
