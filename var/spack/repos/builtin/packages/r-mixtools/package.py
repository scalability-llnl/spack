# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMixtools(RPackage):
    """Tools for Analyzing Finite Mixture Models.

    Analyzes finite mixture models for various parametric and semiparametric
    settings.  This includes mixtures of parametric distributions (normal,
    multivariate normal, multinomial, gamma), various Reliability Mixture
    Models (RMMs), mixtures-of-regressions settings (linear regression,
    logistic regression, Poisson regression, linear regression with
    changepoints, predictor-dependent mixing proportions, random effects
    regressions, hierarchical mixtures-of-experts), and tools for selecting the
    number of components (bootstrapping the likelihood ratio test statistic,
    mixturegrams, and model selection criteria).  Bayesian estimation of
    mixtures-of-linear-regressions models is available as well as a novel data
    depth method for obtaining credible bands.  This package is based upon work
    supported by the National Science Foundation under Grant No.
    SES-0518772."""

    cran = "mixtools"

    license("GPL-2.0-or-later")

    version("2.0.0", sha256="854e7482230b9a5dde61bab191b78e06aa8f9b0cdfe3c03e046afa133b317e0d")
    version("1.2.0", sha256="ef033ef13625209065d26767bf70d129972e6808927f755629f1d70a118b9023")
    version("1.1.0", sha256="543fd8d8dc8d4b6079ebf491cf97f27d6225e1a6e65d8fd48553ada23ba88d8f")
    version("1.0.4", sha256="62f4b0a17ce520c4f8ed50ab44f120e459143b461a9e420cd39056ee4fc8798c")

    depends_on("c", type="build")  # generated

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.2.0:")
    depends_on("r@4.0.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-kernlab", type=("build", "run"), when="@1.2.0:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"), when="@2.0.0:")
    depends_on("r-plotly", type=("build", "run"), when="@2.0.0:")
    depends_on("r-segmented", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
