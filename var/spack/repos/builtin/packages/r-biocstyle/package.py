# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocstyle(RPackage):
    """Standard styles for vignettes and other Bioconductor documents.

       Provides standard formatting styles for Bioconductor PDF and HTML
       documents. Package vignettes illustrate use and functionality."""

    homepage = "https://bioconductor.org/packages/BiocStyle"
    git      = "https://git.bioconductor.org/packages/BiocStyle.git"

    version('2.12.0', commit='0fba3fe6e6a38504f9aadcd3dc95bb83d7e92498')
    version('2.10.0', commit='8fc946044c6b6a8a3104ddbc546baed49ee3aa70')
    version('2.8.2', commit='3210c19ec1e5e0ed8d5a2d31da990aa47b42dbd8')
    version('2.6.1', commit='5ff52cbb439a45575d0f58c4f7a83195a8b7337b')
    version('2.4.1', commit='ef10764b68ac23a3a7a8ec3b6a6436187309c138')

    depends_on('r-bookdown', type=('build', 'run'))
    depends_on('r-knitr@1.12:', type=('build', 'run'))
    depends_on('r-rmarkdown@1.2:', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))

    depends_on('r-biocmanager', when='@2.10.0:', type=('build', 'run'))
