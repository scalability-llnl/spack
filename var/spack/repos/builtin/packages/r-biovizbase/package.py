# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiovizbase(RPackage):
    """Basic graphic utilities for visualization of genomic data..

       The biovizBase package is designed to provide a set of utilities, color
       schemes and conventions for genomic data. It serves as the base for
       various high-level packages for biological data visualization. This
       saves development effort and encourages consistency."""

    homepage = "https://bioconductor.org/packages/biovizBase"
    git      = "https://git.bioconductor.org/packages/biovizBase.git"

    version('1.32.0', commit='de044bf236cdcd71214ae7b77689a8f0ab4f5cc8')
    version('1.30.1', commit='b6776d0470e2920f71127652f185f68ca1fd2c82')
    version('1.28.2', commit='43d09060028665a237b04bfeb9e2575782b08063')
    version('1.26.0', commit='640742f48384f01d117b70dc5c64737e97ae9b4b')
    version('1.24.0', commit='ae9cd2ff665b74a8f45ed9c1d17fc0a778b4af6c')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-dichromat', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', type=('build', 'run'))
    depends_on('r-iranges@1.99.28:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.5.14:', type=('build', 'run'))
    depends_on('r-genomicranges@1.23.21:', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biostrings@2.33.11:', type=('build', 'run'))
    depends_on('r-rsamtools@1.17.28:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.1.16:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.21.19:', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-variantannotation@1.11.4:', type=('build', 'run'))
    depends_on('r-ensembldb@1.99.13:', type=('build', 'run'))
    depends_on('r-annotationfilter@0.99.8:', type=('build', 'run'))

    depends_on('r-rlang', when='@1.28.2:', type=('build', 'run'))
