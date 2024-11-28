# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppad(CMakePackage):
    """A Package for Differentiation of C++ Algorithms."""

    homepage = "https://github.com/coin-or/CppAD"
    url = "https://github.com/coin-or/CppAD/archive/refs/tags/20240000.4.tar.gz"
    git = "https://github.com/coin-or/CppAD.git"

    maintainers("whart222")

    version("master", branch="master")
    version(
        "20240000.4", sha256="0dfc1e30b32d5dd3086ee3adb6d2746a019e9d670b644c4d5ec1df3c35dd1fe5"
    )
    version(
        "20220000.5", sha256="9fb4562f6169855eadcd86ac4671593d1c0edf97bb6ce7cbb28e19af2bfc165e"
    )
    version(
        "20180000.0",
        sha256="a5226e4c5aa2ad6d95668f987b39939315bf134a0a793231984e6d42d6488cca",
        deprecated=True,
    )
    version(
        "20170114",
        sha256="fa3980a882be2a668a7522146273a1b4f1d8dabe66ad4aafa8964c8c1fd6f957",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        # NOTE: This package does not obey CMAKE_INSTALL_PREFIX
        args = [
            self.define("cppad_prefix", self.prefix),
            self.define("CMAKE_BUILD_TYPE", "Release"),
            #
            # Installing documents sometimes fails.
            #
            # self.define("cmake_install_docdir", "share/cppad/doc"),
        ]

        return args
