# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAmpliqueso(RPackage):
    """Analysis of amplicon enrichment panels.

       The package provides tools and reports for the analysis of amplicon
       sequencing panels, such as AmpliSeq"""

    homepage = "https://bioconductor.org/packages/ampliQueso"
    git      = "https://git.bioconductor.org/packages/ampliQueso.git"

    version('1.21.0', commit='ed99c5194a452ee299a93e981da2224e4dab5bdd')
    version('1.20.0', commit='ed064ffe9c5f2b47136e5f0f2e2c4214af4deae8')
    version('1.18.0', commit='c27fa51094135ef8da52cd2b34a27ec6454abd8e')
    version('1.16.0', commit='25d2543ff9dedef4f966f999c95cdf87185d3bb3')
    version('1.14.0', commit='9a4c26ec594171279aba8ab7fe59c4a2ea09b06b')

    depends_on('r@3.6.0:3.6.9', when='@1.21.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.20.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.18.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.14.0', type=('build', 'run'))

    depends_on('r-deseq', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-doparallel', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-edger', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-foreach', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-genefilter', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-ggplot2', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-gplots', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-knitr', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-rgl', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-rnaseqmap@2.17.1:', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-samr', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-statmod', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-variantannotation', when='@1.14.0:', type=('build', 'run'))
    depends_on('r-xtable', when='@1.14.0:', type=('build', 'run'))
