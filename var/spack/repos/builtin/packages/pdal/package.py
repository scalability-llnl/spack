# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pdal(CMakePackage):
    """PDAL is a C++ library for translating and manipulating point cloud data.
    It is very much like the GDAL library which handles raster and vector data.
    """

    homepage = "https://pdal.io"
    url = "https://github.com/PDAL/PDAL/archive/refs/tags/2.6.2.tar.gz"

    maintainers("adamjstewart")

    license("BSD")

    version("2.6.2", sha256="ec4175cfe19dc6b70a0434850f837317f7202f84b63cd8dcc65ca83e04678f57")
    version("2.6.1", sha256="da6e615f01b6110414ef3e2250f112e49df129091abc91ba6866bb01dc68454e")
    version("2.6.0", sha256="12eedeac16ec3aaef42f06078f03f657701c25781207a8e09a3547519228780e")
    version("2.5.6", sha256="de4177305e380d21187da8ec90afda64756bbde5e925035bd53e54a6e349df18")
    version("2.5.5", sha256="6bf4f34bc0bf1bce52b8daecb03a7f45d218c0374bfa00783c787b9e54d56d72")
    version("2.4.3", sha256="e1a910d593311e68b51f32d1f4f8fe4327b97ae7a8de209147b6111091b6f75b")
    version("2.3.0", sha256="8ae848e9b3fe5149a9277fe60e10b9858edb9a3cf1a40728f11712498e5da13a")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.13:", type="build")
    depends_on("gdal@3:")
    depends_on("gdal@3.4:", when="@2.6:")
    depends_on("gdal@:3.6", when="@:2.4")
    depends_on("libgeotiff@1.3.0:")
    depends_on("proj@4.9.3:")

    # https://github.com/PDAL/PDAL/issues/3826
    patch("stdcppfs.patch", when="@:2.4 %gcc@:8")
    msg = "a new stdc++fs patch is needed for version 2.6.2 onwards with gcc@8 or older"
    conflicts("%gcc@:8", when="@2.6.2:", msg=msg)

    def cmake_args(self):
        return [self.define("PROJ_INCLUDE_DIR", self.spec["proj"].prefix.include)]
