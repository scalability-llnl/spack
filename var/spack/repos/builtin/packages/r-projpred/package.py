# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProjpred(RPackage):
    """Projection Predictive Feature Selection.

    Performs projection predictive feature selection for generalized linear
    models and generalized linear and additive multilevel models (see,
    Piironen, Paasiniemi and Vehtari, 2020,
    <https://projecteuclid.org/euclid.ejs/1589335310>, Catalina, Burkner and
    Vehtari, 2020, <arXiv:2010.06994>). The package is compatible with the
    'rstanarm' and 'brms' packages, but other reference models can also be
    used. See the package vignette for more information and examples."""

    cran = "projpred"

    license("GPL-3.0-only OR custom")

    version("2.8.0", sha256="b383ddc5eca275737b96e4e3e14256b4f4abc4b29d292b5cebf3828d0921a1f6")
    version("2.5.0", sha256="b6ec123f5bf573d14cbd5431e3fbdee3215d71d3e263fcbec72bee5930044e39")
    version("2.2.1", sha256="6825ace07d1e580d5916bcd6bfd163460ae9008926f464e00deb7f2395cc72ad")
    version("2.1.2", sha256="a88a651e533c118aad0e8c2c905cfcf688d9c419ed195896036b8f6667b5cfb0")
    version("2.0.2", sha256="af0a9fb53f706090fe81b6381b27b0b6bd3f7ae1e1e44b0ada6f40972b09a55b")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@2.7.0:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"), when="@2.7.0:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"), when="@2.6.0:")
    depends_on("r-rstantools@2.0.0:", type=("build", "run"))
    depends_on("r-loo@2.0.0:", type=("build", "run"))
    depends_on("r-lme4", type=("build", "run"))
    depends_on("r-lme4@1.1-28:", type=("build", "run"), when="@2.5.0:")
    depends_on("r-mvtnorm", type=("build", "run"), when="@2.1.2:")
    depends_on("r-mgcv", type=("build", "run"))
    depends_on("r-gamm4", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"), when="@2.5.0:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-ordinal", type=("build", "run"), when="@2.5.0:")
    depends_on("r-nnet", type=("build", "run"), when="@2.5.0:")
    depends_on("r-mclogit", type=("build", "run"), when="@2.5.0:")
    depends_on("r-rcpparmadillo", type=("build", "run"))

    depends_on("r-ucminf", type=("build", "run"), when="@2.5.0")
    depends_on("r-optimx", type=("build", "run"), when="@:2.0.2")
    depends_on("r-rngtools@1.2.4:", type=("build", "run"), when="@:2.0.2")
    depends_on("r-tidyverse", type=("build", "run"), when="@:2.0.2")
    depends_on("r-dplyr", type=("build", "run"), when="@:2.2.1")
    depends_on("r-magrittr", type=("build", "run"), when="@:2.2.1")
    depends_on("r-rlang", type=("build", "run"), when="@2.1.2:2.2.1")
