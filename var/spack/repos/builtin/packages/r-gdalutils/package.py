# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGdalutils(RPackage):
    """gdalUtils: Wrappers for the Geospatial Data Abstraction Library"""

    homepage = "https://cloud.r-project.org/package=gdalUtils"
    url      = "https://cloud.r-project.org/src/contrib/gdalUtils_2.0.1.14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gdalUtils"

    version('2.0.1.14', sha256='890a502b2eb5f1b23655fab94caad5d32adca05b93f5db1d96d9dcde3f0e7737')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-r-utils', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-rgdal', type=('build', 'run'))
    depends_on('gdal')
