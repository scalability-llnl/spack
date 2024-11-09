# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OmeFilesCpp(CMakePackage):
    """Open Microscopy Environment OME Files is a standalone C++ library for reading
    and writing life sciences image file formats.  It is the reference
    implementation of the OME-TIFF file format.

    """

    homepage = "https://codelibre.gitlab.io/ome/ome-files-cpp/doc/"
    url = "https://gitlab.com/codelibre/ome/ome-files-cpp/-/archive/v0.6.0/ome-files-cpp-v0.6.0.tar.gz"
    git = "https://gitlab.com/codelibre/ome/ome-files-cpp.git"

    maintainers("omsai")

    license("BSD-2-Clause")

    version("master", branch="master")
    version("0.6.0", sha256="e0baf3eeb2ea639f426292a36b58adcaa42ce61a4a0f15f34690602f3f5d47c1")

    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.53: +filesystem +program_options")
    depends_on("ome-model")
    depends_on("ome-model@master", when="@master")
    depends_on("googletest", type="test")

    def cmake_args(self):
        return ["-DCMAKE_CXX_STANDARD=17", "-DCMAKE_CXX_STANDARD_REQUIRED=ON"]
