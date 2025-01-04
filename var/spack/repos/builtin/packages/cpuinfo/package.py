# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Cpuinfo(CMakePackage):
    """cpuinfo is a library to detect essential
    for performance optimization information about host CPU."""

    homepage = "https://github.com/pytorch/cpuinfo"
    git = "https://github.com/pytorch/cpuinfo.git"
    tags = ["windows"]

    license("BSD-2-Clause")

    version("main", branch="main")
    version("2024-09-06", commit="094fc30b9256f54dad5ad23bcbfb5de74781422f")  # py-torch@2.5.1:
    version("2024-08-30", commit="fa1c679da8d19e1d87f20175ae1ec10995cd3dd3")  # py-torch@2.5.0
    version("2023-11-04", commit="d6860c477c99f1fce9e28eb206891af3c0e1a1d7")  # py-torch@2.3:2.4
    version("2023-01-13", commit="6481e8bef08f606ddd627e4d3be89f64d62e1b8a")  # py-torch@2.1:2.2
    version("2022-08-19", commit="8ec7bd91ad0470e61cf38f618cc1f270dede599c")  # py-torch@1.13:2.0
    version("2020-12-17", commit="5916273f79a21551890fd3d56fc5375a78d1598d")  # py-torch@1.8:1.12
    version("2020-06-11", commit="63b254577ed77a8004a9be6ac707f3dccc4e1fd9")  # py-torch@1.6:1.7
    version("2020-01-21", commit="0e6bde92b343c5fbcfe34ecd41abf9515d54b4a7")  # py-torch@1.5
    version("2019-01-17", commit="89fe1695edf9ee14c22f815f24bac45577a4f135")  # py-torch@1.0.1:1.4
    version("2018-10-05", commit="c342292afb040c868849bc15e96ab894dceba2bc")  # py-torch@1.0.0
    version("2018-05-13", commit="1e6c8c99d27f2b5eb9d2e6231055c6a4115b85e5")  # py-torch@0.4.1
    version("2018-04-04", commit="831dc28341b5f20d13e840caf87eaba644d82643")  # py-torch@:0.4.0

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    generator("ninja")
    depends_on("cmake@3.5:", type="build")

    def cmake_args(self):
        # cpuinfo cannot produce a shared build with MSVC because it does not export
        # any symbols
        # cpuinfo CI builds "default" on Windows platform
        build_type = "default" if sys.platform == "win32" else "shared"
        # https://salsa.debian.org/deeplearning-team/cpuinfo/-/blob/master/debian/rules
        return [
            self.define("CPUINFO_BUILD_UNIT_TESTS", False),
            self.define("CPUINFO_BUILD_MOCK_TESTS", False),
            self.define("CPUINFO_BUILD_BENCHMARKS", False),
            self.define("CPUINFO_LIBRARY_TYPE", build_type),
            self.define("CPUINFO_LOG_LEVEL", "error"),
            self.define("CMAKE_SKIP_RPATH", True),
        ]
