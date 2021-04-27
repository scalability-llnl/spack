# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGoDb(RPackage):
    """A set of annotation maps describing the entire Gene Ontology

    A set of annotation maps describing the entire Gene
    Ontology assembled using data from GO."""

    homepage = "https://www.bioconductor.org/packages/GO.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/GO.db_3.4.1.tar.gz"

    version('3.12.1',
            sha256='e0316959d3d32096f9432c897413dff74fce53e15ead7917a7724467d971dab9',
            url='https://bioconductor.org/packages/3.12/data/annotation/src/contrib/GO.db_3.12.1.tar.gz')
    version('3.4.1',
            sha256='2fc2048e9d26edb98e35e4adc4d18c6df54f44836b5cc4a482d36ed99e058cc1',
            url='https://bioconductor.org/packages/3.5/data/annotation/src/contrib/GO.db_3.4.1.tar.gz')

    depends_on('r@2.7.0:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.37.4:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.51.3:', when='@3.12.1:', type=('build', 'run'))
