# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CppTermcolor(CMakePackage):
    """
    Termcolor is a header-only C++ library for printing colored messages to the
    terminal.
    """

    homepage = "https://github.com/ikalnytskyi/termcolor"
    url = "https://github.com/ikalnytskyi/termcolor/archive/refs/tags/v2.0.0.tar.gz"

    maintainers("haampie")

    version("2.0.0", sha256="4a73a77053822ca1ed6d4a2af416d31028ec992fb0ffa794af95bd6216bb6a20")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.0:", type="build")

    def cmake_args(self):
        return [self.define("TERMCOLOR_TESTS", "OFF")]
