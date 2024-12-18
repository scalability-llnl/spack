# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Antlr4CppRuntime(CMakePackage):
    """
    This package provides runtime libraries required to use parsers
    generated for the Cpp language by version 4 of ANTLR (ANother Tool
    for Language Recognition).
    """

    homepage = "https://www.antlr.org"
    url = "https://www.antlr.org/download/antlr4-cpp-runtime-4.13.1-source.zip"
    version("4.13.1", sha256="d350e09917a633b738c68e1d6dc7d7710e91f4d6543e154a78bb964cfd8eb4de")
    version("4.12.0", sha256="642d59854ddc0cebb5b23b2233ad0a8723eef20e66ef78b5b898d0a67556893b")
    version("4.11.1", sha256="8018c335316e61bb768e5bd4a743a9303070af4e1a8577fa902cd053c17249da")
    version("4.10.1", sha256="2a6e602fd593e0a65d8d310c0952bbdfff34ef361362ae87b2a850b62d36f0b6")
    version("4.9.3", sha256="5f0af6efd81f476c3e775c486eb0a71c25d6bbc14373e88a64690e2738d68e03")
    version("4.7.2", sha256="8631a39116684638168663d295a969ad544cead3e6089605a44fea34ec01f31a")

    variant(
        "clanglibcpp", default=False, description="Compile with clang libc++ instead of libstdc++"
    )

    depends_on("uuid", type=["build", "link"], when="@:4.10.1")
    depends_on("git", type=["build"])
    depends_on("pkgconfig", type=["build"])

    def cmake_args(self):
        args = [
            self.define("ANTLR4_INSTALL", "On"),
            self.define("ANTLR_BUILD_CPP_TESTS", "Off"),
            self.define("WITH_DEMO", "Off"),
            self.define("WITH_LIBCXX", "On" if "+clanglibcpp" in self.spec else "Off"),
            self.define("WITH_STATIC_CRT", "Off"),
        ]
        return args
