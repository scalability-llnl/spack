# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OmeModel(CMakePackage):
    """Open Microscopy Environment data model specification, code generator and
    implementation.

    """

    homepage = "https://codelibre.gitlab.io/ome/ome-model/doc/"
    url = "https://gitlab.com/codelibre/ome/ome-model/-/archive/v6.0.0/ome-model-v6.0.0.tar.gz"
    git = "https://gitlab.com/codelibre/ome/ome-model.git"

    maintainers("omsai")

    license("BSD-2-Clause")

    version("master", branch="master")
    version("6.0.0", sha256="d6644ff722411d3a8ac9f26a49c1afda30e4d4102e37b31593d2a9fdc8f96700")

    depends_on("cxx", type="build")  # generated

    # Match version with ome-common-cpp.  It would be nice to match versions in a
    # more automated way.
    depends_on("ome-common-cpp")
    depends_on("ome-common-cpp@master", when="@master")
    depends_on("ome-common-cpp@6.0.0", when="@6.0.0")
    # For running the xsd-fu bundled build tool.
    depends_on("python@3", type="build")
    # From the requirements.txt of xsd-fu
    depends_on("py-genshi", type="build")
    depends_on("py-six", type="build")
    # Optional tests.
    depends_on("googletest", type="test")

    def cmake_args(self):
        return ["-DCMAKE_CXX_STANDARD=17", "-DCMAKE_CXX_STANDARD_REQUIRED=ON"]
