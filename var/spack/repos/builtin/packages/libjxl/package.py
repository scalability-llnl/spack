# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjxl(CMakePackage):
    """JPEG XL image format reference implementation."""

    homepage = "https://github.com/libjxl/libjxl"
    url = "https://github.com/libjxl/libjxl/archive/refs/tags/v0.6.1.tar.gz"
    git = "https://github.com/libjxl/libjxl.git"

    license("Apache-2.0")

    version("main", branch="main", submodules=True)
    version(
        "0.10.2", tag="v0.10.2", commit="e1489592a770b989303b0edc5cc1dc447bbe0515", submodules=True
    )
    version(
        "0.7.0", tag="v0.7.0", commit="f95da131cf7c7ccd4da256356fde2fec1fa23bb5", submodules=True
    )
    version(
        "0.6.1", tag="v0.6.1", commit="a205468bc5d3a353fb15dae2398a101dff52f2d3", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.10:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("brotli")
    depends_on("highway")

    # Only needed at test time, but unfortunately "test" doesn't cause the dep to be added
    # by Spack's compiler wrappers. Solution of adding "link" means that dependency is now
    # always required...
    depends_on("googletest+gmock", type=("link", "test"))

    # https://github.com/libjxl/libjxl/pull/582
    conflicts("%clang", when="@0.6")
    conflicts("%apple-clang", when="@0.6")

    def cmake_args(self):
        args = [
            self.define("JPEGXL_FORCE_SYSTEM_BROTLI", True),
            self.define("JPEGXL_FORCE_SYSTEM_HWY", True),
            self.define("BUILD_TESTING", self.run_tests),
        ]

        if self.run_tests:
            args.append(self.define("JPEGXL_FORCE_SYSTEM_GTEST", True))

        return args
