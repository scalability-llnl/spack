# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVariantannotation(RPackage):
    """Annotation of Genetic Variants.

       Annotate variants, compute amino acid coding changes, predict coding
       outcomes."""

    homepage = "https://bioconductor.org/packages/VariantAnnotation"
    git      = "https://git.bioconductor.org/packages/VariantAnnotation.git"

    version('1.30.1', commit='fb1ab00872570afb280522c4663e347dafc07a9e')
    version('1.28.13', commit='0393347b8ce2d5edf1a61589be93e6a93eda3419')
    version('1.26.1', commit='60ae67598cc3d7ed20ee6417920f8c209085faaf')
    version('1.24.5', commit='468d7f53fd743e04c9af853d58e871b4cc13a090')
    version('1.22.3', commit='3a91b6d4297aa416d5f056dec6f8925eb1a8eaee')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.3:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.4:', type=('build', 'run'))
    depends_on('r-genomicranges@1.27.6:', type=('build', 'run'))
    depends_on('r-summarizedexperiment@1.5.3:', type=('build', 'run'))
    depends_on('r-rsamtools@1.23.10:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.3.25:', type=('build', 'run'))
    depends_on('r-xvector@0.5.6:', type=('build', 'run'))
    depends_on('r-biostrings@2.33.5:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.27.9:', type=('build', 'run'))
    depends_on('r-bsgenome@1.37.6:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.16:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.27.4:', type=('build', 'run'))

    depends_on('r-genomeinfodb@1.15.2:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-summarizedexperiment@1.9.9:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-rsamtools@1.31.2:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.24:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-iranges@2.13.13:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.39.7:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-bsgenome@1.47.3:', when='@1.26.1:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.31.3:', when='@1.26.1:', type=('build', 'run'))

    depends_on('r-rsamtools@1.33.6:', when='@1.28.13:', type=('build', 'run'))

    depends_on('r-rsamtools@1.99.0:', when='@1.30.1:', type=('build', 'run'))
    depends_on('r-rhtslib', when='@1.30.1:', type=('build', 'run'))

    depends_on('gmake', type='build')
