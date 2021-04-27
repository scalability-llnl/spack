# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRunjags(RPackage):
    """Interface Utilities, Model Templates, Parallel Computing Methods and
    Additional Distributions for MCMC Models in JAGS:

    User-friendly interface utilities for MCMC models via Just Another Gibbs
    Sampler (JAGS), facilitating the use of parallel (or distributed)
    processors for multiple chains, automated control of convergence and sample
    length diagnostics, and evaluation of the performance of a model using
    drop-k validation or against simulated data. Template model specifications
    can be generated using a standard lme4-style formula interface to assist
    users less familiar with the BUGS syntax. A JAGS extension module provides
    additional distributions including the Pareto family of distributions, the
    DuMouchel prior and the half-Cauchy prior."""

    homepage = "https://github.com/ku-awdc/runjags"
    cran     = "runjags"

    version('2.2.0-2', sha256='e5dfeb83d36faf19ebe64429f6db64aedecf3c9a040fd5bf9c0200914bf5039a')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-lattice@0.20-10:', type=('build', 'run'))
    depends_on('r-coda@0.17-1:', type=('build', 'run'))
    depends_on('jags@4.3.0:')
