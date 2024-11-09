# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PremakeCore(MakefilePackage):
    """Premake is a command line utility which reads a scripted
    definition of a software project, then uses it to perform
    build configuration tasks or generate project files for
    toolsets like Visual Studio, Xcode, and GNU Make. Premake's
    scripts are little Lua programs, so the sky's the limit!"""

    homepage = "https://premake.github.io/"
    url = "https://github.com/premake/premake-core/archive/v5.0.0-alpha15.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.0.0-alpha15", sha256="188c590f23b944f8fb2a3254acbb63c9655617be021ba4a670d81e6d499ff6cf"
    )
    version(
        "5.0.0-alpha14", sha256="bb0b7b13b1aa175159cbce252389f6e28025a1a935e678632b0dede8e5c21cb9"
    )
    version(
        "5.0.0-alpha13", sha256="bfe983e24686c50cada935f74adad2aefe6581649734b2ab8c1aaa2de4d473c6"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        make("-f", "Bootstrap.mak", self.architecture.platform.name)

    def install(self, spec, prefix):
        install_tree("bin/release", prefix.bin)
