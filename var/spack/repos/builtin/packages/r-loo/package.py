# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RLoo(RPackage):
    """Efficient Leave-One-Out Cross-Validation and WAIC for BayesianModels

    Efficient approximate leave-one-out cross-validation (LOO) for Bayesian
    models fit using Markov chain Monte Carlo, as  described in Vehtari,
    Gelman, and Gabry (2017)  <doi:10.1007/s11222-016-9696-4>.  The
    approximation uses Pareto smoothed importance sampling (PSIS),  a new
    procedure for regularizing importance weights.  As a byproduct of the
    calculations, we also obtain approximate  standard errors for estimated
    predictive errors and for the comparison  of predictive errors between
    models. The package also provides methods  for using stacking and other
    model weighting techniques to average  Bayesian predictive
    distributions."""

    homepage = "https://mc-stan.org/loo"
    url      = "https://cloud.r-project.org/src/contrib/loo_2.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/loo"

    version('2.4.1', sha256='bc21fb6b4a93a7e95ee1be57e4e787d731895fb8b4743c26b30b43adee475b50')
    version('2.3.1', sha256='d98de21b71d9d9386131ae5ba4da051362c3ad39e0305af4f33d830f299ae08b')
    version('2.1.0', sha256='1bf4a1ef85d151577ff96d4cf2a29c9ef24370b0b1eb08c70dcf45884350e87d')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-checkmate', type=('build', 'run'))
    depends_on('r-matrixstats@0.52:', type=('build', 'run'))
    depends_on('pandoc@1.12.3:')
