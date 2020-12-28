# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRios(PythonPackage):
    """Raster I/O Simplification. A set of python modules which makes it easy
       to write raster processing code in Python. Built on top of GDAL, it
       handles the details of opening and closing files, checking alignment of
       projection and raster grid, stepping through the raster in small blocks,
       etc., allowing the programmer to concentrate on the processing involved.
    """

    homepage = "http://rioshome.org"
    url      = "https://github.com/ubarsc/rios/archive/rios-1.4.10.tar.gz"

    version('1.4.10', sha256='7f11b54eb1f2ec551d7fc01c039b60bf2c67f0c2fc5b2946f8d986d6a9bc7063')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('gdal+python', type=('build', 'run'))
