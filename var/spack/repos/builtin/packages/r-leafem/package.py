# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLeafem(RPackage):
    """'leaflet' Extensions for 'mapview'

    Provides extensions for packages 'leaflet' & 'mapdeck', many of which are
    used by package 'mapview'. Focus is on functionality readily available in
    Geographic Information Systems such as 'Quantum GIS'. Includes functions to
    display coordinates of mouse pointer position, query image values via mouse
    pointer and zoom-to-layer buttons. Additionally, provides a feature type
    agnostic function to add points, lines, polygons to a map."""

    homepage = "https://github.com/r-spatial/leafem"
    cran     = "leafem"

    version('0.1.3', sha256='6f123fc15efadb85d317c01003e3b7af5dc925cffe0bbe774b1b39b6bd67f304')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-htmltools@0.3:', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-leaflet@2.0.1:', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
