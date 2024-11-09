# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fxdiv(CMakePackage):
    """Header-only library for division via fixed-point multiplication by inverse."""

    homepage = "https://github.com/Maratyszcza/FXdiv"
    git = "https://github.com/Maratyszcza/FXdiv.git"

    license("MIT")

    version("master", branch="master")
    version("2020-04-17", commit="b408327ac2a15ec3e43352421954f5b1967701d1")  # py-torch@1.6:1.9
    version("2018-11-16", commit="b742d1143724d646cd0f914646f1240eacf5bd73")  # py-torch@1.0:1.5
    version("2018-02-24", commit="811b482bcd9e8d98ad80c6c78d5302bb830184b0")  # py-torch@0.4

    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("python", type="build")

    def cmake_args(self):
        return [
            self.define("FXDIV_BUILD_TESTS", False),
            self.define("FXDIV_BUILD_BENCHMARKS", False),
        ]
