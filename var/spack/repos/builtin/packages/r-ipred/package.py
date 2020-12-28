# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIpred(RPackage):
    """Improved predictive models by indirect classification and bagging for
    classification, regression and survival problems as well as resampling
    based estimators of prediction error."""

    homepage = "https://cloud.r-project.org/package=ipred"
    url      = "https://cloud.r-project.org/src/contrib/ipred_0.9-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ipred"

    version('0.9-9', sha256='0da87a70730d5a60b97e46b2421088765e7d6a7cc2695757eba0f9d31d86416f')
    version('0.9-8', sha256='9c1d11c3cb0d72be7870e70a216e589e403bbfee38c796fe75cd0611d878ac07')
    version('0.9-5', sha256='3a466417808e17c4c6cd0f2b577407355d9da79a341558b42a8b76e24b6f6ba4')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-rpart@3.1-8:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
    depends_on('r-prodlim', type=('build', 'run'))
