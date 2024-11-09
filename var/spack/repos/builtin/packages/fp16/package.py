# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fp16(CMakePackage):
    """FP16 is a header-only library for
    conversion to/from half-precision floating point formats"""

    homepage = "https://github.com/Maratyszcza/FP16/"
    git = "https://github.com/Maratyszcza/FP16.git"

    license("MIT")

    version("master", branch="master")
    version("2020-05-14", commit="4dfe081cf6bcd15db339cf2680b9281b8451eeb3")  # py-torch@1.5:
    version("2018-11-28", commit="febbb1c163726b5db24bed55cc9dc42529068997")  # py-torch@1.1:1.4
    version("2018-10-10", commit="34d4bf01bbf7376f2baa71b8fa148b18524d45cf")  # py-torch@1.0
    version("2018-02-25", commit="43d6d17df48ebf622587e7ed9472ea76573799b9")  # py-torch@:0.4

    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@2.8.12:", type="build")

    resource(
        name="psimd",
        git="https://github.com/Maratyszcza/psimd.git",
        branch="master",
        destination="deps",
        placement="psimd",
    )

    def cmake_args(self):
        return [
            self.define("PSIMD_SOURCE_DIR", join_path(self.stage.source_path, "deps", "psimd")),
            self.define("FP16_BUILD_TESTS", False),
            # https://github.com/Maratyszcza/FP16/issues/21
            self.define("FP16_BUILD_BENCHMARKS", False),
        ]
