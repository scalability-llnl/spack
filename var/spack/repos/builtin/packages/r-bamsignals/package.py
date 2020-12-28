# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBamsignals(RPackage):
    """Extract read count signals from bam files.

       This package allows to efficiently obtain count vectors from indexed bam
       files. It counts the number of reads in given genomic ranges and it
       computes reads profiles and coverage profiles. It also handles paired-
       end data."""

    homepage = "https://bioconductor.org/packages/bamsignals"
    git      = "https://git.bioconductor.org/packages/bamsignals.git"

    version('1.16.0', commit='dba9a4ae1613d2700f122ade1e9b90ca8fce5657')
    version('1.14.0', commit='3107d3a35830e879eeddf127a81016ea1ca9b53d')
    version('1.12.1', commit='06b6282df377cf9db58e8016be4ac8ddcc960939')
    version('1.10.0', commit='7499312ce71e8680680eda10b49d7dff682fc776')
    version('1.8.0', commit='b123b83e8e026c9ec91209d4498aff3e95a5de23')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-rcpp@0.10.6:', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r-rhtslib', type=('build', 'run'))

    depends_on('r-rhtslib@1.12.1:', when='@1.12.1:', type=('build', 'run'))

    depends_on('r-rhtslib@1.13.1:', when='@1.14.0:', type=('build', 'run'))
