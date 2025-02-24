# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatLinnet(RPackage):
    """Linear Networks Functionality of the 'spatstat' Family.

    Defines types of spatial data on a linear network and provides
    functionality for geometrical operations, data analysis and modelling of
    data on a linear network, in the 'spatstat' family of packages. Contains
    definitions and support for linear networks, including creation of
    networks, geometrical measurements, topological connectivity, geometrical
    operations such as inserting and deleting vertices, intersecting a network
    with another object, and interactive editing of networks. Data types
    defined on a network include point patterns, pixel images, functions, and
    tessellations. Exploratory methods include kernel estimation of intensity
    on a network, K-functions and pair correlation functions on a network,
    simulation envelopes, nearest neighbour distance and empty space distance,
    relative risk estimation with cross-validated bandwidth selection. Formal
    hypothesis tests of random pattern (chi-squared, Kolmogorov-Smirnov, Monte
    Carlo, Diggle-Cressie-Loosmore-Ford, Dao-Genton, two-stage Monte Carlo) and
    tests for covariate effects (Cox-Berman-Waller-Lawson, Kolmogorov-Smirnov,
    ANOVA) are also supported. Parametric models can be fitted to point pattern
    data using the function lppm() similar to glm(). Only Poisson models are
    implemented so far. Models may involve dependence on covariates and
    dependence on marks. Models are fitted by maximum likelihood. Fitted point
    process models can be simulated, automatically. Formal hypothesis tests of
    a fitted model are supported (likelihood ratio test, analysis of deviance,
    Monte Carlo tests) along with basic tools for model selection (stepwise(),
    AIC()) and variable selection (sdr). Tools for validating the fitted model
    include simulation envelopes, residuals, residual plots and Q-Q plots,
    leverage and influence diagnostics, partial residuals, and added variable
    plots. Random point patterns on a network can be generated using a variety
    of models."""

    cran = "spatstat.linnet"

    version("3.2-1", sha256="1af0d8063c72650f17c6b79afb07e69e0b6a9794583e8f0c38c6624d91dc11bf")
    version("3.1-0", sha256="b9b0ad66af169ca1ef3da852578d7b65521cf55f4a72c43ae5b1f2d4f47bf00c")
    version("2.3-2", sha256="9c78a4b680debfff0f3ae934575c30d03ded49bc9a7179475384af0ebaf13778")
    version("2.3-1", sha256="119ba6e3da651aa9594f70a7a35349209534215aa640c2653aeddc6aa25038c3")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-spatstat-model@3.2-1:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-model@3.2-11.005:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-spatstat-explore@3.0-6:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-explore@3.2-7.006:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-spatstat-data@2.1-0:", type=("build", "run"))
    depends_on("r-spatstat-data@3.0:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-data@3.0-4:", type=("build", "run"), when="@3.1-5:")
    depends_on("r-spatstat-geom@2.3-0:", type=("build", "run"))
    depends_on("r-spatstat-geom@3.0-6:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-geom@3.2-9.028:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-spatstat-random@2.2-0:", type=("build", "run"), when="@2.3-2:")
    depends_on("r-spatstat-random@3.1-3:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-random@3.2-3.003:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-spatstat-univar@3.0-0:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-spatstat-utils@2.2-0:", type=("build", "run"))
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-spatstat-sparse@2.0:", type=("build", "run"))
    depends_on("r-spatstat-sparse@3.0:", type=("build", "run"), when="@3.1-0:")
    depends_on("r-spatstat-sparse@3.1-0:", type=("build", "run"), when="@3.2-1:")
    depends_on("r-spatstat-core@2.3-2:", type=("build", "run"), when="@2.3-2:2.3-2")
