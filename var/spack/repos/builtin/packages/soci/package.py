# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Soci(CMakePackage):
    """Official repository of the SOCI - The C++ Database Access Library"""

    homepage = "https://github.com/SOCI/soci"
    url = "https://github.com/SOCI/soci/archive/v4.0.2.tar.gz"

    license("BSL-1.0")

    version("4.0.2", sha256="f293192a412ed82693d17dfe46e2734b140bff835bc3259e3cbd7c315e5e2d74")
    version("4.0.0", sha256="359b988d8cbe81357835317821919f7e270c0705e41951a92ac1627cb9fe8faf")
    version(
        "3.2.3",
        sha256="1166664d5d7c4552c4c2abf173f98fa4427fbb454930fd04de3a39782553199e",
        url="https://github.com/SOCI/soci/archive/3.2.3.tar.gz",
    )
    version(
        "3.2.2",
        sha256="cf1a6130ebdf0b84d246da948874ab1312c317e2ec659ede732b688667c355f4",
        url="https://github.com/SOCI/soci/archive/3.2.2.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    variant(
        "cxxstd",
        default=11,
        values=("98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
    )

    variant("static", default=True, description="Enable build of static libraries")
    variant("boost", default=False, description="Build with Boost support")
    variant("sqlite", default=False, description="Build with SQLite support")
    variant("postgresql", default=False, description="Build with PostgreSQL support")

    depends_on("boost", when="+boost")
    depends_on("sqlite", when="+sqlite")
    depends_on("postgresql+client_only", when="+postgresql")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:3"):
            return "src"
        else:
            return self.stage.source_path

    def cmake_args(self):
        args = [
            # SOCI_STATIC does not work with BOOL:OFF
            "-DSOCI_STATIC=" + ("ON" if "+static" in self.spec else "OFF"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("WITH_BOOST", "boost"),
            self.define_from_variant("WITH_SQLITE3", "sqlite"),
            self.define_from_variant("WITH_POSTGRESQL", "postgresql"),
        ]

        return args
