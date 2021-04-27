# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProjpred(RPackage):
    """Projection Predictive Feature Selection:

    Performs projection predictive feature selection for generalized linear
    models and generalized linear and additive multilevel models (see,
    Piironen, Paasiniemi and Vehtari, 2020,
    <https://projecteuclid.org/euclid.ejs/1589335310>, Catalina, Burkner and
    Vehtari, 2020, <arXiv:2010.06994>). The package is compatible with the
    'rstanarm' and 'brms' packages, but other reference models can also be
    used. See the package vignette for more information and examples."""

    homepage = "https://mc-stan.org/projpred/"
    cran     = "projpred"

    version('2.0.2', sha256='af0a9fb53f706090fe81b6381b27b0b6bd3f7ae1e1e44b0ada6f40972b09a55b')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-loo@2.0.0:', type=('build', 'run'))
    depends_on('r-rstantools@2.0.0:', type=('build', 'run'))
    depends_on('r-lme4', type=('build', 'run'))
    depends_on('r-optimx', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rngtools@1.2.4:', type=('build', 'run'))
    depends_on('r-tidyverse', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-gamm4', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
