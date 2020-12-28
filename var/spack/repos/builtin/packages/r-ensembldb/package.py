# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REnsembldb(RPackage):
    """Utilities to create and use Ensembl-based annotation databases.

       The package provides functions to create and use transcript centric
       annotation databases/packages. The annotation for the databases are
       directly fetched from Ensembl using their Perl API. The functionality
       and data is similar to that of the TxDb packages from the
       GenomicFeatures package, but, in addition to retrieve all
       gene/transcript models and annotations from the database, ensembldb
       provides a filter framework allowing to retrieve annotations for
       specific entries like genes encoded on a chromosome region or transcript
       models of lincRNA genes. EnsDb databases built with ensembldb contain
       also protein annotations and mappings between proteins and their
       encoding transcripts. Finally, ensembldb provides functions to map
       between genomic, transcript and protein coordinates."""

    homepage = "https://bioconductor.org/packages/ensembldb"
    git      = "https://git.bioconductor.org/packages/ensembldb.git"

    version('2.8.1', commit='a4d8d89c143dca86b364d59dff8e46cc81c41ac0')
    version('2.6.8', commit='c2c4f41b4ecc81d5328ce1d380065dfcb5e0c54c')
    version('2.4.1', commit='b5b6b94826a2f46a4faecb9dde750ecd3bfaf327')
    version('2.2.2', commit='d71610e58aed88dbbe6a74e7a8ddfb7451398060')
    version('2.0.4', commit='514623d71e3cca7a4e547adb579b5a958702ef86')

    depends_on('r-biocgenerics@0.15.10:', type=('build', 'run'))
    depends_on('r-genomicranges@1.23.21:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.23.18:', type=('build', 'run'))
    depends_on('r-annotationfilter@0.99.7:', type=('build', 'run'))
    depends_on('r-rsqlite@1.1:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-annotationdbi@1.31.19:', type=('build', 'run'))
    depends_on('r-rtracklayer', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-annotationhub', when='@2.0.4:2.2.2', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))

    depends_on('r-genomicfeatures@1.29.10:', when='@2.2.2:', type=('build', 'run'))
    depends_on('r-annotationfilter@1.1.9:', when='@2.2.2:', type=('build', 'run'))
    depends_on('r-iranges@2.11.16:', when='@2.2.2:', type=('build', 'run'))

    depends_on('r-genomicranges@1.31.18:', when='@2.4.1:', type=('build', 'run'))
    depends_on('r-iranges@2.13.24:', when='@2.4.1:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.9:', when='@2.4.1:', type=('build', 'run'))

    depends_on('r-annotationfilter@1.5.2:', when='@2.6.8:', type=('build', 'run'))
