# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtensor(CMakePackage):
    """Multi-dimensional arrays with broadcasting and lazy computing"""

    homepage = "https://github.com/xtensor-stack/xtensor-io"
    url = "https://github.com/QuantStack/xtensor/archive/0.13.1.tar.gz"
    git = "https://github.com/QuantStack/xtensor.git"

    maintainers("ax3l")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("0.24.1", sha256="dd1bf4c4eba5fbcf386abba2627fcb4a947d14a806c33fde82d0cc1194807ee4")
    version("0.24.0", sha256="37738aa0865350b39f048e638735c05d78b5331073b6329693e8b8f0902df713")
    version("0.23.10", sha256="2e770a6d636962eedc868fef4930b919e26efe783cd5d8732c11e14cf72d871c")
    version("0.23.4", sha256="c8377f8ec995762c89dea2fdf4ac06b53ba491a6f0df3421c4719355e42425d2")
    version("0.23.2", sha256="fde26dcf93f5d95996b8cc7e556b84930af41ff699492b7b20b2e3335e12f862")
    version("0.20.7", sha256="b45290d1bb0d6cef44771e7482f1553b2aa54dbf99ef9406fec3eb1e4d01d52b")
    version("0.15.1", sha256="2f4ac632f7aa8c8e9da99ebbfc949d9129b4d644f715ef16c27658bf4fddcdd3")
    version("0.13.1", sha256="f9ce4cd2110386d49e3f36bbab62da731c557b6289be19bc172bd7209b92a6bc")

    depends_on("cxx", type="build")  # generated

    variant("xsimd", default=True, description="Enable SIMD intrinsics")
    variant("tbb", default=True, description="Enable TBB parallelization")

    depends_on("xtl", when="@develop")
    depends_on("xtl@0.7.2:0.7", when="@0.23.2:")
    depends_on("xtl@0.6.4:0.6", when="@0.20.7")
    depends_on("xtl@0.4.0:0.4", when="@0.15.1")
    depends_on("xtl@0.3.3:0.3", when="@0.13.1")
    depends_on("xsimd", when="@develop")

    depends_on("xsimd@8.0.5:", when="@0.24.1: +xsimd")
    depends_on("xsimd@8.0.2:", when="@0.24.0 +xsimd")
    depends_on("xsimd@7.4.10:7", when="@0.23.4:0.23 +xsimd")
    depends_on("xsimd@7.4.9:7", when="@0.23.2 +xsimd")
    depends_on("xsimd@7.2.3:7", when="@0.20.7 +xsimd")
    depends_on("xsimd@4.0.0:4", when="@0.15.1 +xsimd")
    depends_on("xsimd@3.1.0:3", when="@0.13.1 +xsimd")
    depends_on("intel-tbb", when="+tbb")

    # C++14 support
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTS", self.run_tests),
            self.define_from_variant("XTENSOR_USE_XSIMD", "xsimd"),
            self.define_from_variant("XTENSOR_USE_TBB", "tbb"),
        ]

        return args
