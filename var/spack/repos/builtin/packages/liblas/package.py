# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblas(CMakePackage):
    """libLAS is a C/C++ library for reading and writing the very common
    LAS LiDAR format.
    """

    homepage = "https://liblas.org/"
    url = "https://download.osgeo.org/liblas/libLAS-1.8.1.tar.bz2"

    license("BSD-3-Clause")

    version("1.8.1", sha256="9adb4a98c63b461ed2bc82e214ae522cbd809cff578f28511122efe6c7ea4e76")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # libLAS linkage of GDAL and libgeotiff enhances spatial coordinate system
    # description and provides data reprojection support.
    # Ref.: https://liblas.org/compilation.html#optional-libraries
    variant("endian", default=False, description='Build with "Endian-aware" option')
    variant("gdal", default=False, description="Build with GDAL for enhanced performance")
    variant("geotiff", default=True, description="Build with GeoTIFF for enhanced performance")
    variant("laszip", default=False, description="Build with LasZip")

    depends_on("cmake@2.6:", type="build")
    depends_on("libgeotiff@1.3:", when="+geotiff")
    depends_on("boost@1.42:1.72+program_options+thread+system+iostreams+filesystem")
    depends_on("laszip@2.0.1:", when="+laszip")
    depends_on("gdal@1.7:", when="+gdal")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+endian"):
            args.append("-DWITH_ENDIANAWARE=ON")
        else:
            args.append("-DWITH_ENDIANAWARE=OFF")

        if self.spec.satisfies("+gdal"):
            args.append("-DWITH_GDAL=ON")
        else:
            args.append("-DWITH_GDAL=OFF")

        if self.spec.satisfies("+geotiff"):
            args.append("-DWITH_GEOTIFF=ON")
        else:
            args.append("-DWITH_GEOTIFF=OFF")

        if self.spec.satisfies("+laszip"):
            args.append("-DWITH_LASZIP=ON")
        else:
            args.append("-DWITH_LASZIP=OFF")

        return args
