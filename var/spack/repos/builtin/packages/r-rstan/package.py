# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstan(RPackage):
    """User-facing R functions are provided to parse, compile, test, estimate,
    and analyze Stan models by accessing the header-only Stan library provided
    by the 'StanHeaders' package. The Stan project develops a probabilistic
    programming language that implements full Bayesian statistical inference
    via Markov Chain Monte Carlo, rough Bayesian inference via variational
    approximation, and (optionally penalized) maximum likelihood estimation via
    optimization. In all three cases, automatic differentiation is used to
    quickly and accurately evaluate gradients without burdening the user with
    the need to derive the partial derivatives."""

    homepage = "http://mc-stan.org/"
    url      = "https://cloud.r-project.org/src/contrib/rstan_2.10.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rstan"

    version('2.19.2', sha256='31e4ceb9c327cd62873225097ffa538c2ac4cb0547c52271e52e4c7652d508da')
    version('2.18.2', sha256='4d75dad95610d5a1d1c89a4ddbaf4326462e4ffe0ad28aed2129f2d9292e70ff')
    version('2.17.2', sha256='a7b197e6e42f8f0c302da9205afc19a0261eaf6af1425854303d2ce6cbd36729')
    version('2.10.1', sha256='4d2040742607f8675633c6b8c0a2e810f2fe3077f9242b1edfd42642613a8294')

    depends_on('r@3.0.2:', when='@:2.17.3', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@2.18.1:', type=('build', 'run'))
    depends_on('r-stanheaders@2.18.1:', type=('build', 'run'))
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
    depends_on('r-inline', type=('build', 'run'))
    depends_on('r-gridextra@2.0.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
    depends_on('r-loo@2.0.0:', when='@2.18:', type=('build', 'run'))
    depends_on('r-pkgbuild', when='@2.18:', type=('build', 'run'))
    depends_on('r-rcppeigen@0.3.3.3.0:', type=('build', 'run'))
    depends_on('r-bh@1.69.0:', type=('build', 'run'))
    depends_on('gmake', type='build')
    depends_on('pandoc', type='build')

    conflicts('%gcc@:4.9', when='@2.18:')
