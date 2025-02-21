# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ByteLite(CMakePackage):
    """byte lite - A C++17-like byte type for C++98, C++11 and later
    in a single-file header-only library"""

    homepage = "https://github.com/martinmoene/byte-lite"
    url = "https://github.com/martinmoene/byte-lite/archive/refs/tags/v0.3.0.tar.gz"

    license("BSL-1.0", checked_by="pranav-sivaraman")

    version("0.3.0", sha256="1a19e237b12bb098297232b0a74ec08c18ac07ac5ac6e659c1d5d8a4ed0e4813")

    depends_on("cxx", type="build")
    depends_on("cmake@3.5:", type="build")

    conflicts("%gcc@:4.7")
    conflicts("%clang@:3.4")
    conflicts("%apple-clang@:5")
    conflicts("%mvsc@:5")

    def cmake_args(self):
        return [self.define("BYTE_LITE_OPT_BUILD_TESTS", self.run_tests)]
