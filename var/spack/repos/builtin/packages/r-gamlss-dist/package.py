# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamlssDist(RPackage):
    """Distributions for Generalized Additive Models for Location Scale and
    Shape.

    A set of distributions  which can be used  for modelling the response
    variables in Generalized Additive Models for Location Scale and Shape,
    Rigby and Stasinopoulos (2005), <doi:10.1111/j.1467-9876.2005.00510.x>. The
    distributions can be continuous, discrete or mixed  distributions.  Extra
    distributions can be created, by transforming, any continuous distribution
    defined on the real line,  to  a distribution defined on ranges 0 to
    infinity  or  0 to 1,  by using a ''log'' or a ''logit' transformation
    respectively."""

    cran = "gamlss.dist"

    version("6.1-1", sha256="d2db3a7658799c2ef212aa18cb75a3ecf4f73faf8c13dfdc3c14b21ae0129069")
    version("6.0-5", sha256="0f88afdfb148de79d3ece66bf4631ea0dc3ecf1188680802abffd6bc7139a20e")
    version("6.0-3", sha256="ec90ea83cd81b894c73f987f69814077697be33abf0708e0f3e2a39d02c912bf")
    version("6.0-1", sha256="b563b4de6bcedcfa4f8d29198a47004e38fd2de6e0509c788015d4e3feb18154")
    version("5.1-7", sha256="9871c38c893a8df7874c533351858dfe4e7587c71021dbbf88c0c76ff3c0ef5b")
    version("5.1-4", sha256="343c6ca0fd8a1c1dfdf9ffc65c95d4dae0c6c80b3e60fccba003e5171f3d287e")
    version("5.1-3", sha256="87fd643c82579519b67c66c1d87383fa1e203e8b09f607649ee7bce142bda404")
    version("5.1-1", sha256="44f999ff74ee516757eb39c8308c48aa850523aad2f38e622268313a13dda0b1")

    depends_on("r@2.15:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@6.0-3:")
    depends_on("r-mass", type=("build", "run"))
