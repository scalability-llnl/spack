# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scnlib(CMakePackage):
    """scanf for modern C++"""

    homepage = "https://scnlib.dev"
    url = "https://github.com/eliaskosunen/scnlib/archive/refs/tags/v3.0.1.tar.gz"

    maintainers("pranav-sivaraman")

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("3.0.1", sha256="bc8a668873601d00cce6841c2d0f2c93f836f63f0fbc77997834dea12e951eb1")

    variant("shared", default=True, description="Build shared libs")
    variant(
        "regex-backend",
        default="std",
        description="Regex backend to use",
        multi=False,
        values=("std", "Boost"),
    )
    variant(
        "icu",
        default=False,
        description="Use the ICU when using the Boost regex backend",
        when="regex-backend=Boost",
    )

    depends_on("cxx", type="build")
    depends_on("cmake@3.16:", type="build")

    depends_on("fast-float@5:")

    depends_on("boost +regex cxxstd=17", when="regex-backend=Boost")
    depends_on("boost +icu", when="+icu")

    depends_on("googletest cxxstd=17", type="test")
    depends_on("python@3:", type="test")

    def cmake_args(self):
        args = [
            self.define("SCN_TESTS", self.run_tests),
            self.define("SCN_BENCHMARKS", False),
            self.define("SCN_EXAMPLES", False),
            self.define("SCN_DOCS", False),
            self.define("SCN_USE_EXTERNAL_FAST_FLOAT", True),
            self.define("SCN_USE_EXTERNAL_GTEST", True),
            self.define("SCN_USE_EXTERNAL_BENCHMARK", True),
            self.define("SCN_USE_EXTERNAL_REGEX_BACKEND", True),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("SCN_REGEX_BACKEND", "regex-backend"),
        ]

        return args
