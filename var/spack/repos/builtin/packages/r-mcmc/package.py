# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMcmc(RPackage):
    """Markov Chain Monte Carlo:

    Simulates continuous distributions of random vectors using Markov chain
    Monte Carlo (MCMC). Users specify the distribution by an R function that
    evaluates the log unnormalized density. Algorithms are random walk
    Metropolis algorithm (function metrop), simulated tempering (function
    temper), and morphometric random walk Metropolis (Johnson and Geyer, 2012,
    <doi:10.1214/12-AOS1048>, function morph.metrop), which achieves geometric
    ergodicity by change of variable."""

    homepage = "http://www.stat.umn.edu/geyer/mcmc/"
    cran     = "mcmc"

    version('0.9-7', sha256='b7c4d3d5f9364c67a4a3cd49296a61c315ad9bd49324a22deccbacb314aa8260')

    depends_on('r@3.0.2:', type=('build', 'run'))
