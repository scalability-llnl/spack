# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRrcov(RPackage):
    """rrcov: Scalable Robust Estimators with High Breakdown Point"""

    homepage = "https://cloud.r-project.org/package=rrcov"
    url      = "https://cloud.r-project.org/src/contrib/rrcov_1.4-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rrcov"

    version('1.4-7', sha256='cbd08ccce8b583a2f88946a3267c8fc494ee2b44ba749b9296a6e3d818f6f293')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-robustbase@0.92.1:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-pcapp', type=('build', 'run'))
