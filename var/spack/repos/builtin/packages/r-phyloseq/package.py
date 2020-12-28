# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhyloseq(RPackage):
    """Handling and analysis of high-throughput microbiome census data.

       phyloseq provides a set of classes and tools to facilitate the import,
       storage, analysis, and graphical display of microbiome census data."""

    homepage = "https://bioconductor.org/packages/phyloseq"
    git      = "https://git.bioconductor.org/packages/phyloseq.git"

    version('1.28.0', commit='a86ed1e0a650fdf80bee5a0a5a82aaa5a276178d')
    version('1.26.1', commit='a084072bc9e057b90adfbd59e27db2a1ecee151c')
    version('1.24.2', commit='829992f88c79de48bb8749678624e2bbd3b66645')
    version('1.22.3', commit='c695323f2963636d16acda9f05a583bd58e31344')
    version('1.20.0', commit='107d1d5e3437a6e33982c06a548d3cc91df2a7e0')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.18.0:', type=('build', 'run'))
    depends_on('r-ade4@1.7.4:', type=('build', 'run'))
    depends_on('r-ape@3.4:', type=('build', 'run'))
    depends_on('r-biomformat@1.0.0:', type=('build', 'run'))
    depends_on('r-biostrings@2.40.0:', type=('build', 'run'))
    depends_on('r-cluster@2.0.4:', type=('build', 'run'))
    depends_on('r-data-table@1.9.6:', type=('build', 'run'))
    depends_on('r-foreach@1.4.3:', type=('build', 'run'))
    depends_on('r-ggplot2@2.1.0:', type=('build', 'run'))
    depends_on('r-igraph@1.0.1:', type=('build', 'run'))
    depends_on('r-multtest@2.28.0:', type=('build', 'run'))
    depends_on('r-plyr@1.8.3:', type=('build', 'run'))
    depends_on('r-reshape2@1.4.1:', type=('build', 'run'))
    depends_on('r-scales@0.4.0:', type=('build', 'run'))
    depends_on('r-vegan@2.3.5:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))

    depends_on('r@3.4.0:', when='@1.22.3:', type=('build', 'run'))
    depends_on('r-ape@5.0:', when='@1.22.3:', type=('build', 'run'))
    depends_on('r-biobase@2.36.2:', when='@1.22.3:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.22.0:', when='@1.22.3:', type=('build', 'run'))
    depends_on('r-data-table@1.10.4:', when='@1.22.3:', type=('build', 'run'))
    depends_on('r-vegan@2.4:', when='@1.22.3:', type=('build', 'run'))

    depends_on('r-vegan@2.5:', when='@1.24.2:', type=('build', 'run'))
