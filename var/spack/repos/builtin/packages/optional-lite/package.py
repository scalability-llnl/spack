# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from shutil import copytree

from spack.package import *


class OptionalLite(CMakePackage):
    """
    A single-file header-only version of a C++17-like optional, a nullable
    object for C++98, C++11 and later.
    """

    homepage = "https://github.com/martinmoene/optional-lite"
    url = "https://github.com/martinmoene/optional-lite/archive/v3.0.0.tar.gz"

    license("BSL-1.0")

    version("3.6.0", sha256="2be17fcfc764809612282c3e728cabc42afe703b9dc333cc87c48d882fcfc2c2")
    version("3.5.0", sha256="6077cee87e2812afd05a273645051e0b55397a25c220295ddc1d6f49d0cf5cc8")
    version("3.2.0", sha256="069c92f6404878588be761d609b917a111b0231633a91f7f908288fc77eb24c8")
    version("3.1.1", sha256="b61fe644b9f77d7cc1c555b3e40e973b135bf2c0350e5fa67bc6f379d9fc3158")
    version("3.1.0", sha256="66ca0d923e77c3f2a792ef3871e9ddbacf5fac2bfd6b8743df9c9c5814644718")
    version("3.0.0", sha256="36ae58512c478610647978811f0f4dbe105880372bd7ed39417314d50a27254e")
    version("2.3.0", sha256="8fe46216147234b172c6a5b182726834afc44dfdca1e976a264d6f96eb183916")
    version("2.2.0", sha256="9ce1bb021de42f804f8d17ed30b79fc98296122bec8db60492104978cd282fa2")
    version("2.0.0", sha256="e8d803cbc7be241df41a9ab267b525b7941df09747cd5a7deb55f863bd8a4e8d")
    version("1.0.3", sha256="7a2fb0fe20d61d091f6730237add9bab58bc0df1288cb96f3e8a61b859539067")

    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        return [
            f"-DOPTIONAL_LITE_OPT_BUILD_TESTS={'ON' if self.run_tests else 'OFF'}",
            "-DOPTIONAL_LITE_OPT_BUILD_EXAMPLES=OFF",
        ]

    # Pre-3.2.0 install was simply a copytree on the includes
    @when("@:3.1")
    def cmake(self, spec, prefix):
        pass

    @when("@:3.1")
    def build(self, spec, prefix):
        pass

    @when("@:3.1")
    def install(self, spec, prefix):
        copytree("include", prefix.include)

    @when("@:3.1")
    def check(self):
        pass
