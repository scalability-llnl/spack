# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.build_systems import autotools, cmake
from spack.package import *


class Re2c(AutotoolsPackage, CMakePackage):
    """re2c: a free and open-source lexer generator for C and C++"""

    homepage = "https://re2c.org/index.html"
    url = "https://github.com/skvadrik/re2c/releases/download/1.2.1/re2c-1.2.1.tar.xz"
    tags = ["windows"]

    license("Public-Domain")

    version("3.1", sha256="0ac299ad359e3f512b06a99397d025cfff81d3be34464ded0656f8a96676c029")
    version("3.0", sha256="b3babbbb1461e13fe22c630a40c43885efcfbbbb585830c6f4c0d791cf82ba0b")
    version("2.2", sha256="0fc45e4130a8a555d68e230d1795de0216dfe99096b61b28e67c86dfd7d86bda")
    version("2.1.1", sha256="036ee264fafd5423141ebd628890775aa9447a4c4068a6307385d7366fe711f8")
    version("2.1", sha256="8cba0d95c246c670de8f97f57def83a9c0f2113eaa6f7e4867a941f48f633540")

    with default_args(deprecated=True):
        version("2.0.3", sha256="b2bc1eb8aaaa21ff2fcd26507b7e6e72c5e3d887e58aa515c2155fb17d744278")
        version("2.0.2", sha256="6cddbb558dbfd697a729cb4fd3f095524480283b89911ca5221835d8a67ae5e0")
        version("2.0.1", sha256="aef8b50bb75905b2d55a7236380c0efdc756fa077fe16d808aaacbb10fb53531")
        version("2.0", sha256="89a9d7ee14be10e3779ea7b2c8ea4a964afce6e76b8dbcd5479940681db46d20")
        version("1.3", sha256="f37f25ff760e90088e7d03d1232002c2c2672646d5844fdf8e0d51a5cd75a503")
        version("1.2.1", sha256="1a4cd706b5b966aeffd78e3cf8b24239470ded30551e813610f9cd1a4e01b817")

    build_system(conditional("cmake", when="@2.2:"), "autotools", default="autotools")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("python@3.7:", when="@3.1", type="build")

    with when("build_system=cmake"):
        depends_on("cmake@3.12:", type="build")


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        return [
            "--disable-benchmarks",
            "--disable-debug",
            "--disable-dependency-tracking",
            "--disable-docs",
            "--disable-lexers",  # requires existing system re2c
            "--enable-libs",
            "--enable-golang",
        ]


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define("RE2C_BUILD_LIBS", True),
            self.define("RE2C_REBUILD_DOCS", False),
            self.define("RE2C_REBUILD_LEXERS", False),
            self.define("RE2C_REBUILD_PARSERS", False),
            self.define("RE2C_BUILD_RE2RUST", False),
            self.define("RE2C_BUILD_RE2GO", False),
        ]
