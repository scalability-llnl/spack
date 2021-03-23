# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMapview(RPackage):
    """Interactive Viewing of Spatial Data in R

    Quickly and conveniently create interactive visualisations of spatial data
    with or without background maps. Attributes of displayed features are fully
    queryable via pop-up windows. Additional functionality includes methods to
    visualise true- and false-color raster images and bounding boxes."""

    homepage = "https://github.com/r-spatial/mapview"
    cran     = "mapview"

    version('2.9.0', sha256='170cb2b5e67cbeb177f87bd2eab1ecabc44a1042addbcd95a85b2ec4a00eb690')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.6.0:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-leafem', type=('build', 'run'))
    depends_on('r-leaflet@2.0.0:', type=('build', 'run'))
    depends_on('r-leafpop', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-satellite', type=('build', 'run'))
    depends_on('r-scales@0.2.5:', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-webshot', type=('build', 'run'))
    depends_on('gmake', type='build')
