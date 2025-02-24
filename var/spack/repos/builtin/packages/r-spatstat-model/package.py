# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatModel(RPackage):
    """Parametric Statistical Modelling and Inference for the 'spatstat'
    Family.

    Functionality for parametric statistical modelling and inference for
    spatial data, mainly spatial point patterns, in the 'spatstat' family of
    packages. (Excludes analysis of spatial data on a linear network, which is
    covered by the separate package 'spatstat.linnet'.) Supports parametric
    modelling, formal statistical inference, and model validation. Parametric
    models include Poisson point processes, Cox point processes, Neyman-Scott
    cluster processes, Gibbs point processes and determinantal point processes.
    Models can be fitted to data using maximum likelihood, maximum
    pseudolikelihood, maximum composite likelihood and the method of minimum
    contrast. Fitted models can be simulated and predicted. Formal inference
    includes hypothesis tests (quadrat counting tests, Cressie-Read tests,
    Clark-Evans test, Berman test, Diggle-Cressie-Loosmore-Ford test, scan
    test, studentised permutation test, segregation test, ANOVA tests of fitted
    models, adjusted composite likelihood ratio test, envelope tests,
    Dao-Genton test, balanced independent two-stage test), confidence intervals
    for parameters, and prediction intervals for point counts. Model validation
    techniques include leverage, influence, partial residuals, added variable
    plots, diagnostic plots, pseudoscore residual plots, model compensators and
    Q-Q plots."""

    cran = "spatstat.model"

    version("3.3-1", sha256="5c1c969b5f2bbfdfe91ad31cd912f31b91ec9cc7651ecec86c1d7a562161afa7")
    version("3.2-3", sha256="8ad7d2644773571a5c579ceebb98b735dccc97e9b4b109ea39b4ce3faedb14ea")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-spatstat-data@3.0:", type=("build", "run"))
    depends_on("r-spatstat-data@3.0-4:", type=("build", "run"), when="@3.2-11:")
    depends_on("r-spatstat-geom@3.0-5:", type=("build", "run"))
    depends_on("r-spatstat-geom@3.3-0:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-spatstat-random@3.1-4:", type=("build", "run"))
    depends_on("r-spatstat-random@3.3-0:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-spatstat-explore@3.1-0:", type=("build", "run"))
    depends_on("r-spatstat-explore@3.3-0:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-spatstat-univar@3.0-0:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"))
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-spatstat-sparse@3.0:", type=("build", "run"))
    depends_on("r-spatstat-sparse@3.1-0:", type=("build", "run"), when="@3.3-1:")
    depends_on("r-mgcv", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-tensor", type=("build", "run"))
    depends_on("r-goftest@1.2-2:", type=("build", "run"))
