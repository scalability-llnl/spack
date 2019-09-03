# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDelayedmatrixstats(RPackage):
    """Functions that Apply to Rows and Columns of 'DelayedMatrix' Objects.

       A port of the 'matrixStats' API for use with DelayedMatrix objects from
       the 'DelayedArray' package. High-performing functions operating on rows
       and columns of DelayedMatrix objects, e.g. col / rowMedians(), col /
       rowRanks(), and col / rowSds(). Functions optimized per data type and
       for subsetted calculations such that both memory usage and processing
       time is minimized."""

    homepage = "https://bioconductor.org/packages/DelayedMatrixStats"
    git      = "https://git.bioconductor.org/packages/DelayedMatrixStats.git"

    version('1.6.0', commit='0ec517604e940357078540e062b715e3e88a206c')
    version('1.4.0', commit='eb5b390ef99651fe87a346848f807de95afe8971')
    version('1.2.0', commit='de868e730be6280dfad41a280ab09f4d3083c9ac')
    version('1.0.3', commit='e29a3444980ff727c5b12286884b06dfaebf5b5b')

    depends_on('r@3.6.0:3.6.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.4.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.2.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.0.3', type=('build', 'run'))

    depends_on('r-delayedarray', when='@1.0.3:', type=('build', 'run'))
    depends_on('r-iranges', when='@1.0.3:', type=('build', 'run'))
    depends_on('r-matrix', when='@1.0.3:', type=('build', 'run'))
    depends_on('r-matrixstats@0.53.1:', when='@1.0.3:', type=('build', 'run'))
    depends_on('r-s4vectors', when='@1.0.3:', type=('build', 'run'))

    depends_on('r-delayedarray@0.5.27:', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.5:', when='@1.2.0:', type=('build', 'run'))

    depends_on('r-biocparallel', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-delayedarray@0.7.37:', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-hdf5array@1.7.10:', when='@1.4.0:', type=('build', 'run'))

    depends_on('r-delayedarray@0.9.8:', when='@1.6.0:', type=('build', 'run'))
