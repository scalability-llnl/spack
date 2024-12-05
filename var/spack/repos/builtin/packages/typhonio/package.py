# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Typhonio(CMakePackage):
    """TyphonIO is a library of routines that perform input/output (I/O)
    of scientific data within application codes"""

    homepage = "https://uk-mac.github.io/typhonio/"
    url = "https://github.com/UK-MAC/typhonio/archive/v1.6_CMake.tar.gz"
    git = "https://github.com/UK-MAC/typhonio.git"

    license("BSD-3-Clause")

    version("develop", branch="cmake_build")
    version("1.6_CMake", sha256="c9b7b2a7f4fa0b786f6b69c6426b67f42efc4ea6871323139d52cd44f4d0ff7c")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        values=("Debug", "Release"),
        description="The build type to build",
    )
    variant("fortran", default=False, description="Enable Fortran support")
    variant("shared", default=False, description="Build shared libraries")
    variant("doc", default=False, description="Build user guide and doxygen documentation")

    depends_on("mpi")
    depends_on("hdf5+hl")

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "+fortran" in spec:
            cmake_args.append("-DBUILD_FORTRAN_LIBRARY=ON")
        if "+shared" in spec:
            cmake_args.append("-DBUILD_TIO_SHARED=ON")
        if "+docs" in spec:
            cmake_args.append("-DBUILD_DOXYGEN_DOCS=ON")
            cmake_args.append("-DBUILD_USER_GUIDE=ON")

        return cmake_args
