# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSpatialeco(RPackage):
    """Spatial Analysis and Modelling Utilities

    Utilities to support spatial data manipulation, query, sampling and
    modelling. Functions include models for species population density,
    download utilities for climate and global deforestation spatial products,
    spatial smoothing, multivariate separability, point process model for
    creating pseudo- absences and sub-sampling, polygon and point-distance
    landscape metrics, auto-logistic model, sampling models, cluster
    optimization, statistical exploratory tools and raster-based metrics."""

    homepage = "https://cloud.r-project.org/package=spatialEco"
    url      = "https://cloud.r-project.org/src/contrib/spatialEco_1.3-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatialEco"

    version('1.3-5', sha256='d4fb211124edf828333841c44a5af01165c53d89af460144214d81e3c13983c7')
    version('1.3-2', sha256='9dfa427ee8b112446b582f6739a1c40a6e3ad3d050f522082a28ce47c675e57a')
    version('1.3-1', sha256='ff12e26cc1bbf7934fbf712c99765d96ce6817e8055faa15a26d9ebade4bbf1c')
    version('1.3-0', sha256='cfa09673cb3bbed30b243082fc2d63ac09f48b9f072a18d32b95c2c29979d1d0')

    depends_on('r@3.6:', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-spatstat', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-rgeos', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-dplyr', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-exactextractr', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-rcurl', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-rms', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-yaimpute', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-spatialpack@0.3:', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-mgcv', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-envstats', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-cluster', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-readr', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-rann', when='@:1.3-2', type=('build', 'run'))
    depends_on('r-maptools', when='@:1.3-2', type=('build', 'run'))
