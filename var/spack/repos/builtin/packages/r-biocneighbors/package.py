# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocneighbors(RPackage):
    """Nearest Neighbor Detection for Bioconductor Packages.

       Implements exact and approximate methods for nearest neighbor detection,
       in a framework that allows them to be easily switched within
       Bioconductor packages or workflows. Exact searches can be performed
       using the k-means for k-nearest neighbors algorithm or with vantage
       point trees. Approximate searches can be performed using the Annoy or
       HNSW libraries. Searching on either Euclidean or Manhattan distances is
       supported. Parallelization is achieved for all methods by using
       BiocParallel. Functions are also provided to search for all neighbors
       within a given distance."""

    homepage = "https://bioconductor.org/packages/BiocNeighbors"
    git      = "https://git.bioconductor.org/packages/BiocNeighbors.git"

    version('1.2.0', commit='f754c6300f835142536a4594ddf750481e0fe273')
    version('1.0.0', commit='e252fc04b6d22097f2c5f74406e77d85e7060770')

    depends_on('r@3.5:', when='@1.0.0', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-rcppannoy', type=('build', 'run'))

    depends_on('r-biocgenerics', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-rcpphnsw', when='@1.2.0:', type=('build', 'run'))
