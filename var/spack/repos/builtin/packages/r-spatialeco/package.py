# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatialeco(RPackage):
    """Utilities to support spatial data manipulation, query,
       sampling and modelling.
    """

    homepage = "https://cloud.r-project.org/package=spatialEco"
    url      = "https://cloud.r-project.org/src/contrib/spatialEco_1.3-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatialEco"

    version('1.3-2', sha256='9dfa427ee8b112446b582f6739a1c40a6e3ad3d050f522082a28ce47c675e57a')
    version('1.3-1', sha256='ff12e26cc1bbf7934fbf712c99765d96ce6817e8055faa15a26d9ebade4bbf1c')
    version('1.3-0', sha256='cfa09673cb3bbed30b243082fc2d63ac09f48b9f072a18d32b95c2c29979d1d0')

    depends_on('r@3.6:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-exactextractr', type=('build', 'run'))
    depends_on('r-spatstat', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-rms', type=('build', 'run'))
    depends_on('r-yaimpute', type=('build', 'run'))
    depends_on('r-spatialpack@0.3:', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-envstats', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-rgeos', type=('build', 'run'))
    depends_on('r-rann', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-maptools', type=('build', 'run'))
