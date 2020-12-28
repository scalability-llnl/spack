# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomicfeatures(RPackage):
    """Conveniently import and query gene models.

       A set of tools and methods for making and manipulating transcript
       centric annotations. With these tools the user can easily download the
       genomic locations of the transcripts, exons and cds of a given organism,
       from either the UCSC Genome Browser or a BioMart database (more sources
       will be supported in the future). This information is then stored in a
       local database that keeps track of the relationship between transcripts,
       exons, cds and genes. Flexible methods are provided for extracting the
       desired features in a convenient format."""

    homepage = "https://bioconductor.org/packages/GenomicFeatures"
    git      = "https://git.bioconductor.org/packages/GenomicFeatures.git"

    version('1.36.4', commit='28082ec465c91ccaec6881ff348b380edac1b555')
    version('1.34.8', commit='c798b3bb111f4de30632303540074ec1875c1387')
    version('1.32.3', commit='80807d88048858846de3750cecb9431a0e5e69e1')
    version('1.30.3', commit='496bbf81beebd7c934b8d3dcea001e3e4a7d7dee')
    version('1.28.5', commit='ba92381ae93cb1392dad5e6acfab8f6c1d744834')

    depends_on('r-biocgenerics@0.1.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.47:', type=('build', 'run'))
    depends_on('r-iranges@2.9.19:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.11.4:', type=('build', 'run'))
    depends_on('r-genomicranges@1.27.6:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.33.15:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite@2.0:', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-biostrings@2.23.3:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.29.24:', type=('build', 'run'))
    depends_on('r-biomart@2.17.1:', type=('build', 'run'))
    depends_on('r-biobase@2.15.1:', type=('build', 'run'))

    depends_on('r-iranges@2.11.16:', when='@1.30.3:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.13.1:', when='@1.30.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.29.14:', when='@1.30.3:', type=('build', 'run'))
    depends_on('r-rmysql', when='@1.30.3', type=('build', 'run'))

    depends_on('r-s4vectors@0.17.29:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-iranges@2.13.23:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.4:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.17:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.41.4:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.39.7:', when='@1.32.3:', type=('build', 'run'))
