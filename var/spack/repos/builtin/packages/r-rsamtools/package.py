# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRsamtools(RPackage):
    """Binary alignment (BAM), FASTA, variant call (BCF), and tabix file
       import.

       This package provides an interface to the 'samtools', 'bcftools', and
       'tabix' utilities for manipulating SAM (Sequence Alignment / Map),
       FASTA, binary variant call (BCF) and compressed indexed tab-delimited
       (tabix) files."""

    homepage = "https://bioconductor.org/packages/Rsamtools"
    git      = "https://git.bioconductor.org/packages/Rsamtools.git"

    version('2.0.0', commit='dc422f7d56bb604af30fbf33df126d0131d8d77f')
    version('1.34.1', commit='0ec1d45c7a14b51d019c3e20c4aa87c6bd2b0d0c')
    version('1.32.3', commit='0aa3f134143b045aa423894de81912becf64e4c2')
    version('1.30.0', commit='61b365fe3762e796b3808cec7238944b7f68d7a6')
    version('1.28.0', commit='dfa5b6abef68175586f21add7927174786412472')

    depends_on('r@3.6.0:3.6.9', when='@2.0.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.34.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.32.3', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.30.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.28.0', type=('build', 'run'))

    depends_on('r-biocgenerics@0.1.3:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-biocparallel', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-biostrings@2.37.1:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-bitops', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-genomicranges@1.21.6:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-iranges@2.3.7:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.8:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-xvector@0.15.1:', when='@1.28.0:', type=('build', 'run'))
    depends_on('r-zlibbioc', when='@1.28.0:', type=('build', 'run'))

    depends_on('r-biocgenerics@0.25.1:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-biostrings@2.47.6:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.31.8:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-iranges@2.13.12:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@1.32.3:', type=('build', 'run'))
    depends_on('r-xvector@0.19.7:', when='@1.32.3:', type=('build', 'run'))

    depends_on('r-rhtslib@1.15.3:', when='@2.0.0:', type=('build', 'run'))
