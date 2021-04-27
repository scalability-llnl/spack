# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGamlssDist(RPackage):
    """dist: Distributions for Generalized Additive Models for Location Scale
    and Shape

    A set of distributions  which can be used  for modelling the response
    variables in Generalized Additive Models for Location Scale and Shape,
    Rigby and Stasinopoulos (2005), <doi:10.1111/j.1467-9876.2005.00510.x>. The
    distributions can be continuous, discrete or mixed  distributions.  Extra
    distributions can be created, by transforming, any continuous distribution
    defined on the real line,  to  a distribution defined on ranges 0 to
    infinity  or  0 to 1,  by using a ''log'' or a ''logit' transformation
    respectively."""

    homepage = "https://cloud.r-project.org/package=gamlss.dist"
    url      = "https://cloud.r-project.org/src/contrib/gamlss.dist_5.1-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gamlss.dist/"

    version('5.1-7', sha256='9871c38c893a8df7874c533351858dfe4e7587c71021dbbf88c0c76ff3c0ef5b')
    version('5.1-4', sha256='343c6ca0fd8a1c1dfdf9ffc65c95d4dae0c6c80b3e60fccba003e5171f3d287e')
    version('5.1-3', sha256='87fd643c82579519b67c66c1d87383fa1e203e8b09f607649ee7bce142bda404')
    version('5.1-1', sha256='44f999ff74ee516757eb39c8308c48aa850523aad2f38e622268313a13dda0b1')

    depends_on('r@2.15:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
