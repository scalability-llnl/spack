# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatCore(RPackage):
    """Core Functionality of the 'spatstat' Family.

    Functionality for data analysis and modelling of spatial data, mainly
    spatial point patterns, in the 'spatstat' family of packages. (Excludes
    analysis of spatial data on a linear network, which is covered by the
    separate package 'spatstat.linnet'.) Exploratory methods include quadrat
    counts, K-functions and their simulation envelopes, nearest neighbour
    distance and empty space statistics, Fry plots, pair correlation function,
    kernel smoothed intensity, relative risk estimation with cross-validated
    bandwidth selection, mark correlation functions, segregation indices, mark
    dependence diagnostics, and kernel estimates of covariate effects. Formal
    hypothesis tests of random pattern (chi-squared, Kolmogorov-Smirnov, Monte
    Carlo, Diggle-Cressie-Loosmore-Ford, Dao-Genton, two-stage Monte Carlo) and
    tests for covariate effects (Cox-Berman-Waller-Lawson, Kolmogorov-Smirnov,
    ANOVA) are also supported. Parametric models can be fitted to point pattern
    data using the functions ppm(), kppm(), slrm(), dppm() similar to glm().
    Types of models include Poisson, Gibbs and Cox point processes,
    Neyman-Scott cluster processes, and determinantal point processes. Models
    may involve dependence on covariates, inter-point interaction, cluster
    formation and dependence on marks. Models are fitted by maximum likelihood,
    logistic regression, minimum contrast, and composite likelihood methods. A
    model can be fitted to a list of point patterns (replicated point pattern
    data) using the function mppm(). The model can include random effects and
    fixed effects depending on the experimental design, in addition to all the
    features listed above. Fitted point process models can be simulated,
    automatically. Formal hypothesis tests of a fitted model are supported
    (likelihood ratio test, analysis of deviance, Monte Carlo tests) along with
    basic tools for model selection (stepwise(), AIC()) and variable selection
    (sdr). Tools for validating the fitted model include simulation envelopes,
    residuals, residual plots and Q-Q plots, leverage and influence
    diagnostics, partial residuals, and added variable plots."""

    cran = "spatstat.core"

    version("2.4-4", sha256="e38c39efe8b14d6e8fdbee8dd870b90c52f78ea571ab7988fd3685f48347d13b")
    version("2.3-2", sha256="7f4d6d997f9187eda71097a53917e7cbe03f8dcfb4e758d86a90fbe42c92f63c")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-spatstat-data@2.1-0:", type=("build", "run"))
    depends_on("r-spatstat-geom@2.3-0:", type=("build", "run"))
    depends_on("r-spatstat-geom@2.4-0:", type=("build", "run"), when="@2.4-4:")
    depends_on("r-spatstat-random@2.2-0:", type=("build", "run"), when="@2.4-4:")
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-spatstat-utils@2.2-0:", type=("build", "run"))
    depends_on("r-spatstat-utils@2.3.1:", type=("build", "run"), when="@2.4-4:")
    depends_on("r-spatstat-sparse@2.0-0:", type=("build", "run"))
    depends_on("r-mgcv", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-tensor", type=("build", "run"))
    depends_on("r-goftest@1.2-2:", type=("build", "run"))
