# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBrms(RPackage):
    """Bayesian Regression Models using 'Stan'.

    Fit Bayesian generalized (non-)linear multivariate multilevel models using
    'Stan' for full Bayesian inference. A wide range of distributions and link
    functions are supported, allowing users to fit - among others - linear,
    robust linear, count data, survival, response times, ordinal,
    zero-inflated, hurdle, and even self-defined mixture models all in a
    multilevel context. Further modeling options include non-linear and smooth
    terms, auto-correlation structures, censored data, meta-analytic standard
    errors, and quite a few more. In addition, all parameters of the response
    distribution can be predicted in order to perform distributional
    regression. Prior specifications are flexible and explicitly encourage
    users to apply prior distributions that actually reflect their beliefs.
    Model fit can easily be assessed and compared with posterior predictive
    checks and leave-one-out cross-validation.  References: Burkner (2017)
    <doi:10.18637/jss.v080.i01>; Burkner (2018) <doi:10.32614/RJ-2018-017>;
    Carpenter et al. (2017) <doi:10.18637/jss.v076.i01>."""

    cran = "brms"

    license("GPL-2.0-only")

    version("2.21.0", sha256="7289ff33c2a4b83584b7fece0a6aa53fd14b5881a467d417fbca5dbf62ec5d58")
    version("2.19.0", sha256="0e146842c7acfcc6b8273df536eabb5279fb3bf2ae27ce1696f7d838d94fe5c1")
    version("2.18.0", sha256="63914be03cd1c4e6333317d22d7827ba2dc0414cb0dc88337cf74763ba07e111")
    version("2.17.0", sha256="24e5a3a40b81bea558e8f660d0de7fd1a4c2080c7553baac98f34dd2682ece71")
    version("2.16.3", sha256="68302b10b5264f72d163d01c17792c002306cf37f0ee778dcec4c7e118f923e1")
    version("2.16.1", sha256="749efbd9fb061fe207cf2e729c1387d9a8538b922f12ceec4e82a9f8dd9c1bc4")
    version("2.15.0", sha256="c11701d1d8758590b74bb845b568b736e4455a81b114c7dfde0b27b7bd1bcc2f")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@2.20.1:")
    depends_on("r-rcpp@0.12.0:", type=("build", "run"))
    depends_on("r-rstan@2.19.2:", type=("build", "run"))
    depends_on("r-rstan@2.29.0:", type=("build", "run"), when="@2.21.0:")
    depends_on("r-ggplot2@2.0.0:", type=("build", "run"))
    depends_on("r-loo@2.3.1:", type=("build", "run"))
    depends_on("r-posterior@1.0.0:", type=("build", "run"), when="@2.16:")
    depends_on("r-matrix@1.1-1:", type=("build", "run"))
    depends_on("r-mgcv@1.8-13:", type=("build", "run"))
    depends_on("r-rstantools@2.1.1:", type=("build", "run"))
    depends_on("r-bayesplot@1.5.0:", type=("build", "run"))
    depends_on("r-bridgesampling@0.3-0:", type=("build", "run"))
    depends_on("r-glue@1.3.0:", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@2.19.0:")
    depends_on("r-future@1.19.0:", type=("build", "run"))
    depends_on("r-future-apply@1.0.0:", type=("build", "run"), when="@2.21.0:")
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-nleqslv", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-coda", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-backports", type=("build", "run"))

    depends_on("r-shinystan@2.4.0:", type=("build", "run"), when="@:2.20.4")
    depends_on("r-projpred@2.0.0:", type=("build", "run"), when="@:2.16.1")
