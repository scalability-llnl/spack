# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChemometrics(RPackage):
    """R companion to the book "Introduction to Multivariate Statistical
       Analysis in Chemometrics" written by K. Varmuza and P. Filzmoser
       (2009)."""

    homepage = "https://cloud.r-project.org/package=chemometrics"
    url      = "https://cloud.r-project.org/src/contrib/chemometrics_1.4.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/chemometrics"

    version('1.4.2', sha256='b705832fa167dc24b52b642f571ed1efd24c5f53ba60d02c7797986481b6186a')
    version('1.4.1', sha256='7646da0077657d672356204aa2094be68e10ec13617f92ae97ff53a389053905')
    version('1.3.9', sha256='553eda53789b6a4d0f77842c175f98be5b9a04bccc9d2ba0ecde1bb5c8a53f21')
    version('1.3.8', sha256='5a977bf1a9475d4dd4764ec9e99cbce237c5b624ef9aa96fcaf08406b1b8a56d')
    version('1.3.7', sha256='653a4f728c996983a4b5e5144229d0cf8b6754fb7e85e9014eeaf34fa19da42f')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-lars', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-som', type=('build', 'run'))
    depends_on('r-pcapp', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
