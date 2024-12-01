# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Highway(CMakePackage):
    """Performance-portable, length-agnostic SIMD with runtime dispatch."""

    homepage = "https://github.com/google/highway"
    url = "https://github.com/google/highway/archive/refs/tags/1.0.0.tar.gz"

    license("Apache-2.0")

    version("1.2.0", sha256="7e0be78b8318e8bdbf6fa545d2ecb4c90f947df03f7aadc42c1967f019e63343")
    version("1.1.0", sha256="354a8b4539b588e70b98ec70844273e3f2741302c4c377bcc4e81b3d1866f7c9")
    version("1.0.7", sha256="5434488108186c170a5e2fca5e3c9b6ef59a1caa4d520b008a9b8be6b8abe6c5")
    version("1.0.6", sha256="d89664a045a41d822146e787bceeefbf648cc228ce354f347b18f2b419e57207")
    version("1.0.5", sha256="99b7dad98b8fa088673b720151458fae698ae5df9154016e39de4afdc23bb927")
    version("1.0.4", sha256="faccd343935c9e98afd1016e9d20e0b8b89d908508d1af958496f8c2d3004ac2")
    version("1.0.3", sha256="566fc77315878473d9a6bd815f7de78c73734acdcb745c3dde8579560ac5440e")
    version("1.0.2", sha256="e8ef71236ac0d97f12d553ec1ffc5b6375d57b5f0b860c7447dd69b6ed1072db")
    version("1.0.1", sha256="7ca6af7dc2e3e054de9e17b9dfd88609a7fd202812b1c216f43cc41647c97311")
    version("1.0.0", sha256="ab4f5f864932268356f9f6aa86f612fa4430a7db3c8de0391076750197e876b8")

    variant("shared", default=True, description="Build shared libs")
    variant("examples", default=False, description="Build examples")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.10:", type="build")

    depends_on("googletest", type="test")

    def cmake_args(self):
        define = self.define
        from_variant = self.define_from_variant

        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("HWY_ENABLE_EXAMPLES", "examples"),
            define("HWY_ENABLE_TESTS", self.run_tests),
            define("BUILD_TESTING", self.run_tests),
            define("HWY_SYSTEM_GTEST", self.run_tests),
        ]

        return args
