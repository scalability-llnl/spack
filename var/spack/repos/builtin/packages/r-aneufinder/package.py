# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAneufinder(RPackage):
    """Analysis of Copy Number Variation in Single-Cell-Sequencing Data.

       AneuFinder implements functions for copy-number detection, breakpoint
       detection, and karyotype and heterogeneity analysis in single-cell whole
       genome sequencing and strand-seq data."""

    homepage = "https://bioconductor.org/packages/AneuFinder"
    git      = "https://git.bioconductor.org/packages/AneuFinder.git"

    version('1.12.1', commit='e788fd0c864f0bf0abd93df44c6d42f82eb37e0e')
    version('1.10.2', commit='56578ae69abac93dfea6bcac1fc205b14b6ba9dd')
    version('1.8.0', commit='36a729d244add5aafbe21c37a1baaea6a50354d3')
    version('1.6.0', commit='0cfbdd1951fb4df5622e002260cfa86294d65d1d')
    version('1.4.0', commit='e5bdf4d5e4f84ee5680986826ffed636ed853b8e')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-aneufinderdata', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-biocgenerics', when='@1.4.0:1.6.0', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-bamsignals', type=('build', 'run'))
    depends_on('r-dnacopy', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-genomicalignments', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-ggdendro', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
    depends_on('r-reordercluster', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))

    depends_on('r-ecp', when='@1.8.0:', type=('build', 'run'))

    depends_on('r@3.5:', when='@1.10.2:', type=('build', 'run'))
