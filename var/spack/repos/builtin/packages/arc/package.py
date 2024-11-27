# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arc(CMakePackage):
    """ARC is an automatic resiliency library designed to provide security
    to lossy compressed data or other uint8_t data arrays

    forked from: https://github.com/FTHPC/ARC to support Spack after developer
    left grad school
    """

    homepage = "https://github.com/FTHPC/ARC"
    url = "https://github.com/FTHPC/ARC"
    git = "https://github.com/robertu94/ARC"

    maintainers("robertu94")

    version("master", branch="master")
    version("2021-12-01", commit="49d4a5df53a082f15a6959aef434224fd7b9beac")

    depends_on("c", type="build")  # generated

    depends_on("libpressio+sz+zfp", when="+examples")

    variant("examples", description="build examples", default=False)
    variant("shared", description="build shared libraries", default=True)

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_EXAMPLES", "examples"),
        ]
        return args
