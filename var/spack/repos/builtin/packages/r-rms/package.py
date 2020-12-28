# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRms(RPackage):
    """Regression modeling, testing, estimation, validation, graphics,
       prediction, and typesetting by storing enhanced model design
       attributes in the fit. 'rms' is a collection of functions that
       assist with and streamline modeling. It also contains functions
       for binary and ordinal logistic regression models, ordinal models
       for continuous Y with a variety of distribution families, and the
       Buckley-James multiple regression model for right-censored responses,
       and implements penalized maximum likelihood estimation for logistic
       and ordinary linear models. 'rms' works with almost any regression
       model, but it was especially written to work with binary or ordinal
       regression models, Cox regression, accelerated failure time models,
       ordinary linear models, the Buckley-James model, generalized least
       squares for serially or spatially correlated observations,
       generalized linear models, and quantile regression.
    """

    homepage = "https://cloud.r-project.org/package=rms"
    url      = "https://cloud.r-project.org/src/contrib/rms_5.1-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rms"

    version('5.1-4',   sha256='38f5844c4944a95b2adebea6bb1d163111270b8662399ea0349c45c0758076a6')
    version('5.1-3.1', sha256='0946d9547a4e3ff020a61ab3fce38f88aa9545729683e2bfefeb960edec82b37')
    version('5.1-3',   sha256='5fc7120d8a93b4aa9727d82eac368c5c47ff70f467ae2b012afac688235089eb')
    version('5.1-2',   sha256='f1cfeef466ac436105756679353a3468027d97a600e3be755b819aef30ed9207')
    version('5.1-1',   sha256='c489948df5c434b40bcf5288844f5b4e08d157f36939d09230c1600f88d1bfe3')

    depends_on('r@3.5:', type=('build', 'run'))
    depends_on('r-hmisc@4.3:', type=('build', 'run'))
    depends_on('r-survival@3.1-6', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-polspline', type=('build', 'run'))
    depends_on('r-ggplot2@2.2:', type=('build', 'run'))
    depends_on('r-sparsem', type=('build', 'run'))
    depends_on('r-quantreg', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-nlme@3.1-123:', type=('build', 'run'))
    depends_on('r-multcomp', type=('build', 'run'))
    depends_on('r-htmltable@1.11.0:', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
