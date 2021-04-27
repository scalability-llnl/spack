# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyRasterio(PythonPackage):
    """Rasterio reads and writes geospatial raster data.

    Geographic information systems use GeoTIFF and other formats to
    organize and store gridded, or raster, datasets. Rasterio reads
    and writes these formats and provides a Python API based on N-D
    arrays."""

    homepage = "https://github.com/mapbox/rasterio"
    pypi = "rasterio/rasterio-1.1.8.tar.gz"
    git      = "https://github.com/mapbox/rasterio.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('1.1.8',  sha256='f7cac7e2ecf65b4b1eb78c994c63bd429b67dc679b0bc0ecfe487d3d5bf88fd5')
    version('1.1.5',  sha256='ebe75c71f9257c780615caaec8ef81fa4602702cf9290a65c213e1639284acc9')
    version('1.0.24', sha256='4839479621045211f66868ec49625979693450bc2e476f23e7e8ac4804eaf452')
    version('1.0a12', sha256='47d460326e04c64590ff56952271a184a6307f814efc34fb319c12e690585f3c')

    depends_on('python@3.5:', type=('build', 'link', 'run'), when='@1.2:')
    depends_on('python@2.7:2.8,3.5:3.8', type=('build', 'link', 'run'), when='@1.1.0:1.1.999')
    depends_on('python@2.7:2.8,3.5:3.7', type=('build', 'link', 'run'), when='@:1.0')
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type='build', when='@master')
    depends_on('py-affine', type=('build', 'run'))
    depends_on('py-attrs', type=('build', 'run'))
    depends_on('py-click@4:7', type=('build', 'run'))
    depends_on('py-cligj@0.5:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'link', 'run'))
    depends_on('py-snuggs@1.4.1:', type=('build', 'run'))
    depends_on('py-click-plugins', type=('build', 'run'))
    depends_on('py-enum34', type='run', when='^python@:3.3')
    depends_on('gdal@3.0:', when='@1.2.0:')
    depends_on('gdal@1.11:3.2', when='@1.1.0:1.1.999')
    depends_on('gdal@1.11:3.0', when='@1.0.25:1.0.999')
    depends_on('gdal@1.11:2', when='@:1.0.24')
