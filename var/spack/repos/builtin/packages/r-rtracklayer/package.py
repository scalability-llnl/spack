# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRtracklayer(RPackage):
    """R interface to genome annotation files and the UCSC genome browser.

       Extensible framework for interacting with multiple genome browsers
       (currently UCSC built-in) and manipulating annotation tracks in various
       formats (currently GFF, BED, bedGraph, BED15, WIG, BigWig and 2bit
       built-in). The user may export/import tracks to/from the supported
       browsers, as well as query and modify the browser state, such as the
       current viewport."""

    homepage = "https://bioconductor.org/packages/rtracklayer"
    git      = "https://git.bioconductor.org/packages/rtracklayer.git"

    version('1.44.4', commit='aec96e85daf53b5c5eb2e89250d2755352be4de3')
    version('1.42.2', commit='76702f671faea736807d54aeecfbadcd152d94c5')
    version('1.40.6', commit='ba9a6e711504a702147383bc7abfcc36eb304df7')
    version('1.38.3', commit='f20db703c09dc7e808c09e9b78c15aec9e546248')
    version('1.36.6', commit='8c0ac7230f94e0c5a981acbb178c8de70e968131')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.21.20:', type=('build', 'run'))
    depends_on('r-xml@1.98-0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.13.8:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.3.7:', type=('build', 'run'))
    depends_on('r-xvector@0.9.4:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.3.14:', type=('build', 'run'))
    depends_on('r-biostrings@2.43.7:', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-rcurl@1.4-2:', type=('build', 'run'))
    depends_on('r-rsamtools@1.17.8:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.5.4:', type=('build', 'run'))

    depends_on('r-iranges@2.11.12:', when='@1.38.3:', type=('build', 'run'))

    depends_on('r-genomicranges@1.31.8:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.25.1:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-iranges@2.13.13:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.15.2:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-rsamtools@1.31.2:', when='@1.40.6:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.15.6:', when='@1.40.6:', type=('build', 'run'))

    depends_on('r-s4vectors@0.19.22:', when='@1.42.2:', type=('build', 'run'))
