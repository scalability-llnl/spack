# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScater(RPackage):
    """Single-Cell Analysis Toolkit for Gene Expression Data in R.

       A collection of tools for doing various analyses of single-cell RNA-seq
       gene expression data, with a focus on quality control and
       visualization."""

    homepage = "https://bioconductor.org/packages/scater"
    git      = "https://git.bioconductor.org/packages/scater.git"

    version('1.12.2', commit='1518dc27a87c79181c34107d639e95fe55e55092')
    version('1.10.1', commit='2e6694af2929092f263c2b0830d48b3f9632e70c')
    version('1.8.4', commit='d560a9a378541d53d17990d2aa2cd28874df3dcd')
    version('1.6.3', commit='964effb4e883102d7c8cae627dbac4ba5d216a75')
    version('1.4.0', commit='90a2eab66ff82ba6dd7fbb33e41cd0ded20fa218')

    depends_on('r@3.3:', when='@1.4.0', type=('build', 'run'))
    depends_on('r-biobase', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-biomart', when='@1.4.0:1.6.3', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-data-table', when='@1.4.0:1.6.3', type=('build', 'run'))
    depends_on('r-dplyr', when='@1.4.0:1.12.2', type=('build', 'run'))
    depends_on('r-edger', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-ggbeeswarm', type=('build', 'run'))
    depends_on('r-limma', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-matrixstats', when='@1.4.0:1.6.3', type=('build', 'run'))
    depends_on('r-plyr', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-reshape2', when='@1.4.0:1.10.1', type=('build', 'run'))
    depends_on('r-rhdf5', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-rjson', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-shiny', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-shinydashboard', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-tximport', when='@1.4.0:1.8.4', type=('build', 'run'))
    depends_on('r-viridis', type=('build', 'run'))

    depends_on('r@3.4:', when='@1.6.3', type=('build', 'run'))
    depends_on('r-singlecellexperiment', when='@1.6.3:', type=('build', 'run'))
    depends_on('r-summarizedexperiment', when='@1.6.3:', type=('build', 'run'))
    depends_on('r-s4vectors', when='@1.6.3:', type=('build', 'run'))
    depends_on('r-rcpp', when='@1.6.3:', type=('build', 'run'))
    depends_on('r-rhdf5lib', when='@1.6.3:1.10.1', type=('build', 'run'))
    depends_on('r-beachmat', when='@1.6.3:', type=('build', 'run'))

    depends_on('r@3.5:', when='@1.8.4', type=('build', 'run'))
    depends_on('r-delayedmatrixstats', when='@1.8.4:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.14:', when='@1.8.4:', type=('build', 'run'))
    depends_on('r-delayedarray', when='@1.8.4:', type=('build', 'run'))

    depends_on('r-biocparallel', when='@1.10.1:', type=('build', 'run'))

    depends_on('r@3.6:', when='@1.12.2', type=('build', 'run'))
    depends_on('r-biocneighbors', when='@1.12.2:', type=('build', 'run'))
    depends_on('r-biocsingular', when='@1.12.2:', type=('build', 'run'))
