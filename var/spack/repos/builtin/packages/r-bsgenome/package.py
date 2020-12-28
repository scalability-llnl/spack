# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBsgenome(RPackage):
    """Software infrastructure for efficient representation of full genomes and
       their SNPs."""

    homepage = "https://bioconductor.org/packages/BSgenome"
    git      = "https://git.bioconductor.org/packages/BSgenome.git"

    version('1.52.0', commit='5398eba1cb56a873b29c04a7ce6858d5d60ff75b')
    version('1.50.0', commit='43910755f7477e4fe9bb968f186fddbb2f7355f9')
    version('1.48.0', commit='092a1b90482ace329cbd8ca2a338e91449acb93e')
    version('1.46.0', commit='bdfbd6d09820993585b8231ddea5e11c99008dc5')
    version('1.44.2', commit='105b00588a758d5ec7c347a7dff2756aea4516a0')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.8:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.36:', type=('build', 'run'))
    depends_on('r-iranges@2.1.33:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.4:', type=('build', 'run'))
    depends_on('r-genomicranges@1.27.6:', type=('build', 'run'))
    depends_on('r-biostrings@2.35.3:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.8:', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))

    depends_on('r-iranges@2.11.16:', when='@1.46.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.46.0:', type=('build', 'run'))
    depends_on('r-genomicranges@1.29.14:', when='@1.46.0:', type=('build', 'run'))

    depends_on('r-s4vectors@0.17.28:', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-iranges@2.13.16:', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.2:', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.10:', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.48.0:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.39.7:', when='@1.48.0:', type=('build', 'run'))
