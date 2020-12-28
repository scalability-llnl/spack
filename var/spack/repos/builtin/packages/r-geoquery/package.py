# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeoquery(RPackage):
    """Get data from NCBI Gene Expression Omnibus (GEO).

       The NCBI Gene Expression Omnibus (GEO) is a public repository of
       microarray data. Given the rich and varied nature of this resource, it
       is only natural to want to apply BioConductor tools to these data.
       GEOquery is the bridge between GEO and BioConductor."""

    homepage = "https://bioconductor.org/packages/GEOquery"
    git      = "https://git.bioconductor.org/packages/GEOquery.git"

    version('2.52.0', commit='3059331eb82ad4947c2d1bef86ff9526e70af643')
    version('2.50.5', commit='135c17f8fe535acda14f95a37d1be1ff2bd80f97')
    version('2.48.0', commit='6a8d1ca195b5c26fb717ae93beb1a8d9b7031c5e')
    version('2.46.15', commit='a52b195ac640caae9679610d5b486b7cb828c0fd')
    version('2.42.0', commit='c26adef8d3ddbd6932a3170f2f84f6e4327641fb')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-xml', when='@2.42.0', type=('build', 'run'))
    depends_on('r-rcurl', when='@2.42.0', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))

    depends_on('r-readr', when='@2.46.15:', type=('build', 'run'))
    depends_on('r-xml2', when='@2.46.15:', type=('build', 'run'))
    depends_on('r-dplyr', when='@2.46.15:', type=('build', 'run'))
    depends_on('r-tidyr', when='@2.46.15:', type=('build', 'run'))
    depends_on('r-magrittr', when='@2.46.15:', type=('build', 'run'))
    depends_on('r-limma', when='@2.46.15:', type=('build', 'run'))

    depends_on('r-readr@1.3.1:', when='@2.50.5:', type=('build', 'run'))
