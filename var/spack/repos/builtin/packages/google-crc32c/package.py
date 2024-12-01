# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GoogleCrc32c(CMakePackage):
    """CRC32C implementation with support for CPU-specific acceleration instructions."""

    homepage = "https://github.com/google/crc32c"
    url = "https://github.com/google/crc32c/archive/refs/tags/1.1.2.tar.gz"

    maintainers("marcusboden")

    license("BSD-3-Clause")

    version("1.1.2", sha256="ac07840513072b7fcebda6e821068aa04889018f24e10e46181068fb214d7e56")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")

    def cmake_args(self):
        args = [
            self.define("CRC32C_BUILD_TESTS", False),
            self.define("CRC32C_BUILD_BENCHMARKS", False),
            self.define("CRC32C_USE_GLOG", False),
            self.define("BUILD_SHARED_LIBS", True),
        ]
        return args
