# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PrometheusCpp(CMakePackage):
    """Prometheus Client Library for Modern C++."""

    homepage = "https://jupp0r.github.io/prometheus-cpp/"
    url = "https://github.com/jupp0r/prometheus-cpp/releases/download/v1.2.4/prometheus-cpp-with-submodules.tar.gz"
    git = "https://github.com/jupp0r/prometheus-cpp.git"

    license("MIT", checked_by="mdorier")

    version("master", branch="master", submodules=True)
    version("1.2.4", sha256="0d6852291063c35853e88805c73b52f73c0c08b78c1e7bc4d588fcf72a7172eb")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake@3.14.0:", type="build")
    depends_on("zlib")
    depends_on("curl")

    def cmake_args(self):
        args = ["-DBUILD_SHARED_LIBS=ON", "-DENABLE_TESTING=OFF"]
        return args
