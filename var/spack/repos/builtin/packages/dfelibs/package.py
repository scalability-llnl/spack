# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dfelibs(CMakePackage):
    """Acts fork of dfelibs, a header-only utility library for C++."""

    homepage = "https://github.com/acts-project/dfelibs"
    url = "https://github.com/acts-project/dfelibs/archive/refs/tags/v20211029.tar.gz"

    maintainers("stephenswat", "wdconinc")

    license("MIT", checked_by="stephenswat")

    version("20231012", sha256="7127069858c2e3ce663e66f45e3f7e02ede8bbca23d90f6c89f43f5b05c44dcb")
    version("20211029", sha256="65b8d536b06b550e38822905dea06d193beb703fe0e4442791f43dc087c5cbfb")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.8:", type="build")
    depends_on("boost@1.59:", type="test")

    def cmake_args(self):
        args = [
            self.define("dfelibs_BUILD_EXAMPLES", False),
            self.define("dfelibs_BUILD_UNITTESTS", self.run_tests),
        ]

        return args
