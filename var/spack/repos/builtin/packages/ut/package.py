# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ut(CMakePackage):
    """UT: C++20 μ(micro)/Unit Testing Framework"""

    homepage = "https://boost-ext.github.io/ut"
    url = "https://github.com/boost-ext/ut/archive/v0.0.0.tar.gz"
    git = "https://github.com/boost-ext/ut.git"

    maintainers("msimberg")

    license("BSL-1.0")

    version("master", branch="master")
    version("2.0.1", sha256="1e43be17045a881c95cedc843d72fe9c1e53239b02ed179c1e39e041ebcd7dad")
    version("2.0.0", sha256="8b5b11197d1308dfc1fe20efd6a656e0c833dbec2807e2292967f6e2f7c0420f")
    version("1.1.9", sha256="1a666513157905aa0e53a13fac602b5673dcafb04a869100a85cd3f000c2ed0d")

    depends_on("cxx", type="build")

    generator("ninja")

    depends_on("cmake@3.21:3.25", type="build", when="@master")
    depends_on("cmake@3.12:3.20", type="build", when="@1.1.9")
    depends_on("ninja", type="build")

    conflicts("%gcc@:8")
    conflicts("%clang@:8")
    conflicts("%clang@:10", when="platform=darwin")

    # 1.1.9 had the version set to 1.1.8. See: https://github.com/boost-ext/ut/pull/492.
    patch(
        "https://github.com/boost-ext/ut/pull/492.patch?full_index=1",
        sha256="1858aefec7e6adbb6130bf32a0343f9ddd173182f9dba3eb3d30523e11d26987",
        when="@1.1.9",
    )

    def cmake_args(self):
        return [
            self.define("BOOST_UT_BUILD_BENCHMARKS", False),
            self.define("BOOST_UT_BUILD_EXAMPLES", False),
            self.define("BOOST_UT_BUILD_TESTS", self.run_tests),
        ]
