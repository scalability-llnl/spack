# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kcov(CMakePackage):
    """Code coverage tool for compiled programs, Python and Bash which uses
    debugging information to collect and report data without special
    compilation options"""

    homepage = "https://simonkagstrom.github.io/kcov/index.html"
    url = "https://github.com/SimonKagstrom/kcov/archive/refs/tags/v42.tar.gz"

    license("GPL-2.0-or-later")

    version("42", sha256="2c47d75397af248bc387f60cdd79180763e1f88f3dd71c94bb52478f8e74a1f8")
    version(
        "38",
        sha256="b37af60d81a9b1e3b140f9473bdcb7975af12040feb24cc666f9bb2bb0be68b4",
        url="https://github.com/SimonKagstrom/kcov/archive/38.tar.gz",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.4:", type="build")
    depends_on("zlib-api")
    depends_on("curl")
    depends_on("elfutils", when="platform=linux")
    depends_on("binutils +libiberty", when="platform=linux", type="link")

    def cmake_args(self):
        # Necessary at least on macOS, fixes linking error to LLDB
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/kcov.rb
        return ["-DSPECIFY_RPATH=ON"]

    def test_kcov_help(self):
        """run installed kcov help"""
        kcov = Executable(self.prefix.bin.kcov)
        # The help message exits with an exit code of 1
        kcov("-h", ignore_errors=1)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        self.test_kcov_help()
