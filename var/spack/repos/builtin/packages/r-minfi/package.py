# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMinfi(RPackage):
    """Analyze Illumina Infinium DNA methylation arrays.

       Tools to analyze & visualize Illumina Infinium methylation arrays."""

    homepage = "https://bioconductor.org/packages/minfi"
    git      = "https://git.bioconductor.org/packages/minfi.git"

    version('1.30.0', commit='a4c28e9388fe3b35e7d21a9669e39250ed6dcbcd')
    version('1.28.4', commit='b5125b2f3e05d37d519eeb6fd44a60efdad388e7')
    version('1.26.2', commit='ebb07b728b2453998d46e4e53d4fbf873e8e81fc')
    version('1.24.0', commit='a4df428588ea86a1c79ddba76132014f0a39644e')
    version('1.22.1', commit='b2faf84bcbb291e32d470a0e029450093527545b')

    depends_on('r-biocgenerics@0.15.3:', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment@1.1.6:', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-bumphunter@1.1.9:', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-genomeinfodb', type=('build', 'run'))
    depends_on('r-biobase@2.33.2:', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-beanplot', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nor1mix', type=('build', 'run'))
    depends_on('r-siggenes', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-illuminaio', type=('build', 'run'))
    depends_on('r-matrixstats@0.50.0:', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-reshape', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-geoquery', type=('build', 'run'))

    depends_on('r-delayedmatrixstats', when='@1.26.2:', type=('build', 'run'))
    depends_on('r-delayedarray@0.5.23:', when='@1.26.2:', type=('build', 'run'))
    depends_on('r-hdf5array', when='@1.26.2:', type=('build', 'run'))
    depends_on('r-biocparallel', when='@1.26.2:', type=('build', 'run'))

    depends_on('r-illuminaio@0.23.2:', when='@1.28.4:', type=('build', 'run'))
    depends_on('r-delayedmatrixstats@1.3.4:', when='@1.28.4:', type=('build', 'run'))
    depends_on('r-delayedarray@0.7.38:', when='@1.28.4:', type=('build', 'run'))

    depends_on('r-delayedarray@0.9.8:', when='@1.30.0:', type=('build', 'run'))
