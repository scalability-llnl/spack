# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5cpp(CMakePackage):
    """Easy to use HDF5 C++ templates for Serial and Parallel HDF5"""

    homepage = "http://h5cpp.org"
    url = "https://github.com/steven-varga/h5cpp/archive/v1.10.4-5.tar.gz"
    git = "https://github.com/steven-varga/h5cpp.git"

    maintainers("eschnett")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.10.4-6", sha256="4fbc8e777dc78a37ec2fe8c7b6a47114080ffe587f083e83a2046b5e794aef93")
    version("1.10.4-5", sha256="661ccc4d76e081afc73df71ef11d027837d92dd1089185f3650afcaec9d418ec")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Include MPI support")

    depends_on("cmake @3.10:", type="build")
    depends_on("hdf5 @1.10.4:")
    depends_on("hdf5 +mpi", when="+mpi")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        return [
            "-DHDF5_INCLUDE_DIRS=%s" % self.spec["hdf5"].headers.directories[0],
            "-DHDF5_LIBRARIES=%s" % self.spec["hdf5"].libs.directories[0],
            "-DH5CPP_BUILD_TESTS=OFF",
        ]
