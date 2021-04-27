# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RNimble(RPackage):
    """MCMC, Particle Filtering, and Programmable Hierarchical Modeling

    A system for writing hierarchical statistical models largely compatible
    with 'BUGS' and 'JAGS', writing nimbleFunctions to operate models and do
    basic R-style math, and compiling both models and nimbleFunctions via
    custom-generated C++. 'NIMBLE' includes default methods for MCMC, Monte
    Carlo Expectation Maximization, and some other tools. The nimbleFunction
    system makes it easy to do things like implement new MCMC samplers from R,
    customize the assignment of samplers to different parts of a model from R,
    and compile the new samplers automatically via C++ alongside the samplers
    'NIMBLE' provides. 'NIMBLE' extends the 'BUGS'/'JAGS' language by making it
    extensible: New distributions and functions can be added, including as
    calls to external compiled code. Although most people think of MCMC as the
    main goal of the 'BUGS'/'JAGS' language for writing models, one can use
    'NIMBLE' for writing arbitrary other kinds of model-generic algorithms as
    well. A full User Manual is available at <https://r-nimble.org>."""

    homepage = "https://cloud.r-project.org/package=nimble"
    url      = "https://cloud.r-project.org/src/contrib/nimble_0.9.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nimble"

    version('0.10.1', sha256='11e248fda442f233c3590640efd9381c9b4b2e6fb66dce45a3391db03b70e702')
    version('0.9.1', sha256='ad5e8a171193cb0172e68bf61c4f94432c45c131a150101ad1c5c7318c335757')
    version('0.9.0', sha256='ebc28fadf933143eea73900cacaf96ff81cb3c2d607405016062b7e93afa5611')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('gmake', type='build')
