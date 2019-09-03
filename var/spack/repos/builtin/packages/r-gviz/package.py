# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGviz(RPackage):
    """Plotting data and annotation information along genomic coordinates

       Genomic data analyses requires integrated visualization of known genomic
       information and new experimental data. Gviz uses the biomaRt and the
       rtracklayer packages to perform live annotation queries to Ensembl and
       UCSC and translates this to e.g. gene/transcript structures in viewports
       of the grid graphics package. This results in genomic information
       plotted together with your data."""

    homepage = "https://bioconductor.org/packages/Gviz"
    git      = "https://git.bioconductor.org/packages/Gviz.git"

    version('1.28.0', commit='c51ad68d6ccee1ad1cf79ca44b22869991dfc9ce')
    version('1.26.5', commit='430310b9d2e098f9757a71d26a2f69871071f30c')
    version('1.24.0', commit='3ee1eec97a56653c07c434a97f82cfe3c4281841')
    version('1.22.3', commit='2238079d0a7017c474f010acb35d98ee7cc1c5d1')
    version('1.20.0', commit='299b8255e1b03932cebe287c3690d58c88f5ba5c')

    depends_on('r@3.6.0:3.6.9', when='@1.28.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.26.5', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.24.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.22.3', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.20.0', type=('build', 'run'))

    depends_on('r-annotationdbi@1.27.5:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-biobase@2.15.3:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.11.3:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-biomart@2.11.0:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-biostrings@2.33.11:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-biovizbase@1.13.8:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-bsgenome@1.33.1:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-digest(>=@0.6.8:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.1.16:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-genomicfeatures@1.17.22:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-genomicranges@1.17.20:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-iranges@1.99.18:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-lattice', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-latticeextra@0.6-26:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-matrixstats@0.8.14:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-rsamtools@1.17.28:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.13:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', when='@1.20.0:', type=('build', 'run'))
    depends_on('r-xvector@0.5.7:', when='@1.20.0:', type=('build', 'run'))
