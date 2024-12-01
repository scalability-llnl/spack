# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OmeCommonCpp(CMakePackage):
    """Open Microscopy Environment: Common functionality for OME C++ libraries and
    applications which is not readily available from the C++ Standard Library.
    This includes basic portability functions, to wrapping other libraries to
    make them usable with Modern C++ programming practices.

    """

    homepage = "https://gitlab.com/codelibre/ome/ome-common-cpp"
    url = "https://gitlab.com/codelibre/ome/ome-common-cpp/-/archive/v6.0.0/ome-common-cpp-v6.0.0.tar.gz"
    git = "https://gitlab.com/codelibre/ome/ome-common-cpp.git"

    maintainers("omsai")

    license("BSD-2-Clause")

    version("master", branch="master")
    version("6.0.0", sha256="26f3ce6e0b9a022590eed2ade5519eca12a2507bb207cdfe9f29d360984a7e0d")

    depends_on("cxx", type="build")  # generated

    depends_on("fmt")
    depends_on("spdlog")
    depends_on("xalan-c")
    depends_on("googletest", type="test")

    def cmake_args(self):
        return ["-DCMAKE_CXX_STANDARD=17", "-DCMAKE_CXX_STANDARD_REQUIRED=ON"]
