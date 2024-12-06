# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPivy(PythonPackage):
    """Python bindings to coin3d"""

    homepage = "https://github.com/coin3d/pivy"
    url = "https://github.com/coin3d/pivy/archive/refs/tags/0.6.8.tar.gz"

    license("0BSD")

    version("0.6.8", sha256="c443dd7dd724b0bfa06427478b9d24d31e0c3b5138ac5741a2917a443b28f346")

    depends_on("cxx", type="build")  # generated

    depends_on("coin3d")
    depends_on("py-setuptools", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("swig", type="build")

    def patch(self):
        # https://github.com/coin3d/pivy/issues/93
        filter_file(
            "project(pivy_cmake_setup NONE)",
            "project(pivy_cmake_setup)",
            "distutils_cmake/CMakeLists.txt",
            string=True,
        )
