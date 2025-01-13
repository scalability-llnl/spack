# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstat(RPackage):
    """Spatial Point Pattern Analysis, Model-Fitting, Simulation, Tests.

    Comprehensive open-source toolbox for analysing Spatial Point Patterns.
    Focused mainly on two-dimensional point patterns, including
    multitype/marked points, in any spatial region. Also supports
    three-dimensional point patterns, space-time point patterns in any number
    of dimensions, point patterns on a linear network, and patterns of other
    geometrical objects. Supports spatial covariate data such as pixel images.
    Contains over 2000 functions for plotting spatial data, exploratory data
    analysis, model-fitting, simulation, spatial sampling, model diagnostics,
    and formal inference. Data types include point patterns, line segment
    patterns, spatial windows, pixel images, tessellations, and linear
    networks. Exploratory methods include quadrat counts, K-functions and their
    simulation envelopes, nearest neighbour distance and empty space
    statistics, Fry plots, pair correlation function, kernel smoothed
    intensity, relative risk estimation with cross-validated bandwidth
    selection, mark correlation functions, segregation indices, mark dependence
    diagnostics, and kernel estimates of covariate effects. Formal hypothesis
    tests of random pattern (chi-squared, Kolmogorov-Smirnov, Monte Carlo,
    Diggle-Cressie-Loosmore-Ford, Dao-Genton, two-stage Monte Carlo) and tests
    for covariate effects (Cox-Berman-Waller-Lawson, Kolmogorov-Smirnov, ANOVA)
    are also supported. Parametric models can be fitted to point pattern data
    using the functions ppm(), kppm(), slrm(), dppm() similar to glm(). Types
    of models include Poisson, Gibbs and Cox point processes, Neyman-Scott
    cluster processes, and determinantal point processes. Models may involve
    dependence on covariates, inter-point interaction, cluster formation and
    dependence on marks. Models are fitted by maximum likelihood, logistic
    regression, minimum contrast, and composite likelihood methods. A model can
    be fitted to a list of point patterns (replicated point pattern data) using
    the function mppm(). The model can include random effects and fixed effects
    depending on the experimental design, in addition to all the features
    listed above. Fitted point process models can be simulated, automatically.
    Formal hypothesis tests of a fitted model are supported (likelihood ratio
    test, analysis of deviance, Monte Carlo tests) along with basic tools for
    model selection (stepwise(), AIC()) and variable selection (sdr). Tools for
    validating the fitted model include simulation envelopes, residuals,
    residual plots and Q-Q plots, leverage and influence diagnostics, partial
    residuals, and added variable plots."""

    cran = "spatstat"

    license("GPL-2.0-or-later")

    version("3.1-1", sha256="5649309818c6e76c8b8ee7b66a25dcbd2b358d90da56f67dd961b5cf9ff55512")
    version("3.0-5", sha256="b926ed55dfeb95b09fb441f44d85204277eee00e42ac258c0a08baa1ce263bb1")
    version("2.3-4", sha256="4ea0f8d70b926b92bf4a06521f985a0bb6d573619f5d526957c87860ccb999da")
    version("2.3-0", sha256="da02443722f2c7ef9d59a2799b7b8002c94cecf73f2b0d2b29280d39f49c4c06")
    version("1.64-1", sha256="ca3fc7d0d6b7a83fd045a7502bf03c6871fa1ab2cf411647c438fd99b4eb551a")
    version("1.63-3", sha256="07b4a1a1b37c91944f31779dd789598f4a5ad047a3de3e9ec2ca99b9e9565528")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.3-0:")
    depends_on("r-spatstat-model@3.2-3:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-model@3.3-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-explore@3.1-0:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-explore@3.3-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-data@1.4-2:", type=("build", "run"))
    depends_on("r-spatstat-data@2.1-0:", type=("build", "run"), when="@2.3-0:")
    depends_on("r-spatstat-data@2.1-2:", type=("build", "run"), when="@2.3-4:")
    depends_on("r-spatstat-data@3.0-1:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-data@3.1-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-geom@2.3-0:", type=("build", "run"), when="@2.3-0:")
    depends_on("r-spatstat-geom@2.4-0:", type=("build", "run"), when="@2.3-4:")
    depends_on("r-spatstat-geom@3.1-0:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-geom@3.3-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-random@2.2-0:", type=("build", "run"), when="@2.3-4:")
    depends_on("r-spatstat-random@3.1-4:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-random@3.3-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-linnet@2.3-0:", type=("build", "run"), when="@2.3-0:")
    depends_on("r-spatstat-linnet@2.3-2:", type=("build", "run"), when="@2.3-4:")
    depends_on("r-spatstat-linnet@3.1-0:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-linnet@3.2-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-univar@3.0-0:", type=("build", "run"), when="@3.1-1:")
    depends_on("r-spatstat-utils@1.17:", type=("build", "run"))
    depends_on("r-spatstat-utils@2.2-0:", type=("build", "run"), when="@2.3-0:")
    depends_on("r-spatstat-utils@2.3-0:", type=("build", "run"), when="@2.3-4:")
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"), when="@3.0-5:")
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@3.1-1:")

    depends_on("r-rpart", type=("build", "run"), when="@:1.64-1")
    depends_on("r-nlme", type=("build", "run"), when="@:1.64-1")
    depends_on("r-mgcv", type=("build", "run"), when="@:1.64-1")
    depends_on("r-matrix", type=("build", "run"), when="@:1.64-1")
    depends_on("r-deldir@0.0-21:", type=("build", "run"), when="@:1.64-1")
    depends_on("r-abind", type=("build", "run"), when="@:1.64-1")
    depends_on("r-tensor", type=("build", "run"), when="@:1.64-1")
    depends_on("r-polyclip@1.10:", type=("build", "run"), when="@:1.64-1")
    depends_on("r-goftest@1.2-2:", type=("build", "run"), when="@:1.64-1")
    depends_on("r-spatstat-core@2.3-0:", type=("build", "run"), when="@2.3-0:2.3-4")
    depends_on("r-spatstat-core@2.4-1:", type=("build", "run"), when="@2.3-4:2.3-4")
