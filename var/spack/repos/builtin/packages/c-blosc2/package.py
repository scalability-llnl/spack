# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CBlosc2(CMakePackage):
    """Next generation c-blosc with a new API, a new container and
    other bells and whistles"""

    homepage = "https://www.blosc.org/"
    url = "https://github.com/Blosc/c-blosc2/archive/refs/tags/v2.15.1.tar.gz"
    git = "https://github.com/Blosc/c-blosc2.git"

    maintainers("ax3l", "robert-mijakovic")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("2.15.1", sha256="6cf32fcfc615542b9ba35e021635c8ab9fd3d328fd99d5bf04b7eebc80f1fae2")
    version("2.11.1", sha256="1e9923e0f026eb6e6caee608b4b9a523837806076fc79409055a6386cf5de1ea")
    version("2.10.5", sha256="a88f94bf839c1371aab8207a6a43698ceb92c72f65d0d7fe5b6e59f24c138b4d")
    # 2.10.2+ fixes regressions with external dependencies
    version("2.10.2", sha256="069785bc14c006c7dab40ea0c620bdf3eb8752663fd55c706d145bceabc2a31d")
    # 2.10.1+ adds Blosc2 CMake CONFIG files
    version("2.10.1", sha256="1dd65be2d76eee205c06e8812cc1360448620eee5e368b25ade4ea310654cd01")
    version("2.10.0", sha256="cb7f7c0c62af78982140ecff21a2f3ca9ce6a0a1c02e314fcdce1a98da0fe231")
    version("2.9.3", sha256="1f36b7d79d973505582b9a804803b640dcc0425af3d5e676070847ac4eb38176")
    version("2.2.0", sha256="66f9977de26d6bc9ea1c0e623d873c3225e4fff709aa09b3335fd09d41d57c0e")
    version("2.1.1", sha256="a8cbedefb8ed3b83629534ec8b4a822ffcdb1576e13dfb93107361551d32e6e9")
    version("2.1.0", sha256="a9570f4101654c2fe2a706adcab0821cdbcf7523fcb6602407dda21b67fdacfd")
    version("2.0.4", sha256="90c78edcc262759dd16d243141513310624bb4fda3d98ac34dcfb78255e151c1")
    version("2.0.2", sha256="fba51ba601610441eea6046e384284b2d8d7884922060cf15369d01d713b9b77")
    version("2.0.1", sha256="35b93dfed479b1dfd9372d41d7843b60254ed1d71792577b95e489c28705874f")

    depends_on("c", type="build")  # generated

    variant("avx2", default=True, description="Enable AVX2 support")

    variant("lizard", default=True, description="support for LIZARD (LZ5)")
    variant("lz4", default=True, description="support for LZ4")
    variant("snappy", default=True, description="support for SNAPPY")
    variant("zlib", default=True, description="support for ZLIB")
    variant("zstd", default=True, description="support for ZSTD")

    depends_on("cmake@3.16.3:", type="build")
    depends_on("lizard", when="+lizard")
    depends_on("lz4", when="+lz4")
    depends_on("snappy", when="+snappy")
    depends_on("zlib-api", when="+zlib")
    depends_on("zstd", when="+zstd")

    conflicts("%oneapi")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DDEACTIVATE_LZ4={0}".format("ON" if "~lz4" in spec else "OFF"),
            "-DDEACTIVATE_LIZARD={0}".format("ON" if "~lizard" in spec else "OFF"),
            "-DDEACTIVATE_SNAPPY={0}".format("ON" if "~snappy" in spec else "OFF"),
            "-DDEACTIVATE_ZLIB={0}".format("ON" if "~zlib" in spec else "OFF"),
            "-DDEACTIVATE_ZSTD={0}".format("ON" if "~zstd" in spec else "OFF"),
            "-DPREFER_EXTERNAL_LIZARD=ON",
            "-DPREFER_EXTERNAL_LZ4=ON",
            # snappy is supported via external install only
            "-DPREFER_EXTERNAL_ZLIB=ON",
            "-DPREFER_EXTERNAL_ZSTD=ON",
            "-DDEACTIVATE_AVX2={0}".format("ON" if "~avx2" in spec else "OFF"),
            self.define("BUILD_TESTS", self.run_tests),
            self.define("BUILD_BENCHMARKS", self.run_tests),
            self.define("BUILD_EXAMPLES", self.run_tests),
            self.define("BUILD_FUZZERS", self.run_tests),
        ]

        return args
