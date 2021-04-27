# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGbm(RPackage):
    """Generalized Boosted Regression Models

    An implementation of extensions to Freund and Schapire's AdaBoost
    algorithm and Friedman's gradient boosting machine. Includes regression
    methods for least squares, absolute loss, t-distribution loss, quantile
    regression, logistic, multinomial logistic, Poisson, Cox proportional
    hazards  partial likelihood, AdaBoost exponential loss, Huberized hinge
    loss, and  Learning to Rank measures (LambdaMart). Originally developed by
    Greg Ridgeway."""

    homepage = "https://cloud.r-project.org/package=gbm"
    url      = "https://cloud.r-project.org/src/contrib/gbm_2.1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gbm"

    version('2.1.8', sha256='7d5de3b980b8f23275e86ac9bed48a497c9aa53c58e407dfd676309f38272ec1')
    version('2.1.5', sha256='06fbde10639dfa886554379b40a7402d1f1236a9152eca517e97738895a4466f')
    version('2.1.3', sha256='eaf24be931d762f1ccca4f90e15997719d01005f152160a3d20d858a0bbed92b')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-gridextra', when='@2.1.5', type=('build', 'run'))
