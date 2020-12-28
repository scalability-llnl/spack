# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgdal(RPackage):
    """Provides bindings to the 'Geospatial' Data Abstraction Library
    ('GDAL') (>= 1.6.3) and access to projection/transformation operations
    from the 'PROJ.4' library. The 'GDAL' and 'PROJ.4' libraries are
    external to the package, and, when installing the package from source,
    must be correctly installed first. Both 'GDAL' raster and 'OGR' vector
    map data can be imported into R, and 'GDAL' raster data and 'OGR'
    vector data exported. Use is made of classes defined in the 'sp' package.
    Windows and Mac Intel OS X binaries (including 'GDAL', 'PROJ.4' and
    'Expat') are provided on 'CRAN'."""

    homepage = "https://cloud.r-project.org/package=rgdal"
    url      = "https://cloud.r-project.org/src/contrib/rgdal_1.3-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rgdal"

    version('1.5-18', sha256='53467c19bc93d8ea311458eaa281c8c456168ab75e84d76ef5cc6c00f53122df')
    version('1.4-4',  sha256='2532e76e0af27d145f799d70006a5dbecb2d3be698e3d0bbf580f4c41a34c5d7')
    version('1.3-9',  sha256='3e44f88d09894be4c0abd8874d00b40a4a5f4542b75250d098ffbb3ba41e2654')
    version('1.2-16', sha256='017fefea4f9a6d4540d128c707197b7025b55e4aff98fc763065366b025b03c9')

    depends_on('r@3.5.0:', when='@1.5:', type=('build', 'run'))
    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-sp@1.1-0:', type=('build', 'run'))
    depends_on('gdal@1.11.4:')
    depends_on('proj@4.8.0:5', when='@:1.3-9')
    depends_on('proj@4.8.0:', when='@1.4-2:')
