# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lodepng(MakefilePackage):
    """PNG encoder and decoder in C and C++."""

    homepage = "https://lodev.org/lodepng/"
    git = "https://github.com/lvandeve/lodepng.git"

    license("Zlib")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("sdl2")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        for exe in ["unittest", "benchmark", "pngdetail", "showpng"]:
            install(exe, prefix.bin)
