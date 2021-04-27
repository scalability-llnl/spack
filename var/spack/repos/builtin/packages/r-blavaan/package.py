# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBlavaan(RPackage):
    """Bayesian Latent Variable Analysis:

    Fit a variety of Bayesian latent variable models, including confirmatory
    factor analysis, structural equation models, and latent growth curve
    models."""

    cran     = "blavaan"

    version('0.3-15', sha256='f73ead024bc3b65bdb0c5e5cd5458845158914eb579c07be2fd697a3573ebe6f')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-lavaan@0.6-5:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.15:', type=('build', 'run'))
    depends_on('r-rcppparallel@5.0.1:', type=('build', 'run'))
    depends_on('r-mcmcpack', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-nonnest2@0.5-5:', type=('build', 'run'))
    depends_on('r-loo@2.0:', type=('build', 'run'))
    depends_on('r-rstan@2.19.2:', type=('build', 'run'))
    depends_on('r-rstantools@1.5.0:', type=('build', 'run'))
    depends_on('r-bayesplot', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-future-apply', type=('build', 'run'))
    depends_on('r-stanheaders@2.18.1:', type=('build', 'run'))
    depends_on('r-bh@1.69.0:', type=('build', 'run'))
    depends_on('r-rcppeigen@0.3.3.4.0:', type=('build', 'run'))
    depends_on('gmake', type='build')
