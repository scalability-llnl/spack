# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStatmod(RPackage):
    """A collection of algorithms and functions to aid statistical
    modeling. Includes growth curve comparisons, limiting dilution
    analysis (aka ELDA), mixed linear models, heteroscedastic
    regression, inverse-Gaussian probability calculations, Gauss
    quadrature and a secure convergence algorithm for nonlinear
    models. Includes advanced generalized linear model functions
    that implement secure convergence, dispersion modeling and
    Tweedie power-law families."""

    homepage = "https://cloud.r-project.org/package=statmod"
    url      = "https://cloud.r-project.org/src/contrib/statmod_1.4.30.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/statmod"

    version('1.4.32', sha256='2f67a1cfa66126e6345f8a40564a3077d08f1748f17cb8c8fb05c94ed0f57e20')
    version('1.4.30', sha256='9d2c1722a85f53623a9ee9f73d835119ae22ae2b8ec7b50d675401e314ea641f')

    depends_on('r@3.0.0:', type=('build', 'run'))
