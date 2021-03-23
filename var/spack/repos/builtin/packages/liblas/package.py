# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Liblas(CMakePackage):
    """libLAS is a C/C++ library for reading and writing the very common
    LAS LiDAR format.
    """

    homepage = "https://liblas.org/"
    url      = "https://download.osgeo.org/liblas/libLAS-1.8.1.tar.bz2"

    version('1.8.1', sha256='9adb4a98c63b461ed2bc82e214ae522cbd809cff578f28511122efe6c7ea4e76')

    # libLAS linkage of GDAL and libgeotiff enhances spatial coordinate system
    # description and provides data reprojection support.
    # Ref.: https://liblas.org/compilation.html#optional-libraries
    variant('endian',  default=False, description='Build with "Endian-aware" option')
    variant('gdal',    default=False, description='Build with GDAL for enhanced performance')
    variant('geotiff', default=True,  description='Build with GeoTIFF for enhanced performance')
    variant('laszip',  default=False, description='Build with LasZip')

    depends_on('libgeotiff')
    depends_on('boost@:1.69.0')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('laszip', when='+laszip')
    depends_on('gdal', when='+gdal')

    def cmake_args(self):
        args = []
        if '+endian' in self.spec:
            args.append('-DWITH_ENDIANAWARE=ON')
        else:
            args.append('-DWITH_ENDIANAWARE=OFF')

        if '+gdal' in self.spec:
            args.append('-DWITH_GDAL=ON')
        else:
            args.append('-DWITH_GDAL=OFF')

        if '+geotiff' in self.spec:
            args.append('-DWITH_GEOTIFF=ON')
        else:
            args.append('-DWITH_GEOTIFF=OFF')

        if '+laszip' in self.spec:
            args.append('-DWITH_LASZIP=ON')
        else:
            args.append('-DWITH_LASZIP=OFF')

        return args
