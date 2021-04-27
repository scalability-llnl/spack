# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBayesplot(RPackage):
    """Plotting for Bayesian Models:

    Plotting functions for posterior analysis, MCMC diagnostics, prior and
    posterior predictive checks, and other visualizations to support the
    applied Bayesian workflow advocated in Gabry, Simpson, Vehtari, Betancourt,
    and Gelman (2019) <doi:10.1111/rssa.12378>. The package is designed not
    only to provide convenient functionality for users, but also a common set
    of functions that can be easily used by developers working on a variety of
    R packages for Bayesian modeling, particularly (but not exclusively)
    packages interfacing with 'Stan'."""

    homepage = "https://mc-stan.org/bayesplot/"
    cran     = "bayesplot"

    version('1.8.0', sha256='a605f9929e681593a3ef3ca9c836e713314994aaea00f359f71cfc42d151c948')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-dplyr@0.8.0:', type=('build', 'run'))
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-ggridges', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-tidyselect', type=('build', 'run'))
