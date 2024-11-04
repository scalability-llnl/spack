# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MagicEnum(CMakePackage):
    """Header-only C++17 library provides static reflection for enums,
    work with any enum type without any macro or boilerplate code."""

    homepage = "https://github.com/Neargye/magic_enum"
    url = "https://github.com/Neargye/magic_enum/archive/refs/tags/v0.9.6.tar.gz"

    maintainers("pranav-sivaraman")

    license("MIT", checked_by="pranav-sivaraman")

    version("0.9.6", sha256="814791ff32218dc869845af7eb89f898ebbcfa18e8d81aa4d682d18961e13731")

    variant("examples", default=False, description="Enable examples")

    with default_args(msg="Compiler version is too old"):
        conflicts("%clang@:4")
        conflicts("%gcc@:8")
        conflicts("%msvc@:14.10")
        conflicts("%apple-clang@:9")

    depends_on("cxx", type="build")

    depends_on("cmake@3.14:", type="build")

    def cmake_args(self):
        define = self.define
        from_variant = self.define_from_variant

        args = [
            define("MAGIC_ENUM_OPT_BUILD_TESTS", self.run_tests),
            from_variant("MAGIC_ENUM_OPT_BUILD_EXAMPLES", "examples"),
        ]

        return args
