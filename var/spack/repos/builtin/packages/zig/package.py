# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Zig(CMakePackage):
    """A general-purpose programming language and toolchain for maintaining
    robust, optimal, and reusable software.
    """

    homepage = "https://ziglang.org/"
    git = "https://github.com/ziglang/zig.git"

    maintainers("alalazo")

    license("MIT")

    version("0.13.0", tag="0.13.0", commit="cf90dfd3098bef5b3c22d5ab026173b3c357f2dd")
    version("0.12.0", tag="0.12.0", commit="a685ab1499d6560c523f0dbce2890dc140671e43")
    version("0.11.0", tag="0.11.0", commit="67709b638224ac03820226c6744d8b6ead59184c")
    version("0.10.1", tag="0.10.1", commit="b57081f039bd3f8f82210e8896e336e3c3a6869b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        values=("Release", "RelWithDebInfo", "MinSizeRel"),
        default="Release",
        description="CMake build type",
    )

    depends_on("llvm targets=all")
    depends_on("llvm@15", when="@0.10.1")
    depends_on("llvm@16", when="@0.11.0")
    depends_on("llvm@17", when="@0.12.0")
    depends_on("llvm@18", when="@0.13.0")

    depends_on("git", type="build")
    depends_on("ccache")

    provides("ziglang")

    def cmake_args(self):
        return [
            self.define("ZIG_USE_CCACHE", True),
            self.define("ZIG_STATIC_LLVM", True),
            self.define("ZIG_STATIC_ZLIB", True),
        ]
