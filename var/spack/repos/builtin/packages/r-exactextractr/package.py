# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RExactextractr(RPackage):
    """Provides a replacement for the 'extract' function from the 'raster'
       package that is suitable for extracting raster values using 'sf'
       polygons.
    """

    homepage = "https://cloud.r-project.org/package=exactextractr"
    url      = "https://cloud.r-project.org/src/contrib/exactextractr_0.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/exactextractr"

    version('0.3.0', sha256='c7fb38b38b9dc8b3ca5b8f1f84f4ba3256efd331f2b4636b496d42689ffc3fb0')
    version('0.2.1', sha256='d0b998c77c3fd9265a600a0e08e9bf32a2490a06c19df0d0c0dea4b5c9ab5773')

    depends_on('r@3.4:', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-rcpp@0.12.12:', type=('build', 'run'))
    depends_on('geos@3.5:', type=('build', 'run', 'link'))
