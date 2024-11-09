# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gflags(CMakePackage):
    """The gflags package contains a C++ library that implements
    commandline flags processing. It includes built-in support for
    standard types such as string and the ability to define flags
    in the source file in which they are used. Online documentation
    available at: https://gflags.github.io/gflags/"""

    homepage = "https://gflags.github.io/gflags"
    url = "https://github.com/gflags/gflags/archive/v2.1.2.tar.gz"

    license("BSD-3-Clause")

    version("2.2.2", sha256="34af2f15cf7367513b352bdcd2493ab14ce43692d2dcd9dfc499492966c64dcf")
    version("2.1.2", sha256="d8331bd0f7367c8afd5fcb5f5e85e96868a00fd24b7276fa5fcee1e5575c2662")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.12:", type="build")

    def cmake_args(self):
        return ["-DBUILD_SHARED_LIBS=ON"]
