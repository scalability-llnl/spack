# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFlexclust(RPackage):
    """The main function kcca implements a general framework for k-centroids
    cluster analysis supporting arbitrary distance measures and centroid
    computation. Further cluster methods include hard competitive learning,
    neural gas, and QT clustering. There are numerous visualization methods for
    cluster results (neighborhood graphs, convex cluster hulls, barcharts of
    centroids, ...), and bootstrap methods for the analysis of cluster
    stability."""

    homepage = "https://cloud.r-project.org/package=flexclust"
    url      = "https://cloud.r-project.org/src/contrib/flexclust_1.3-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/flexclust"

    version('1.4-0', sha256='82fe445075a795c724644864c7ee803c5dd332a89ea9e6ccf7cd1ae2d1ecfc74')
    version('1.3-5', sha256='dbf49969c93a7b314d9dc3299a0764ed9a804ba7dcbdc08a1235f244f4b85059')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-modeltools', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
