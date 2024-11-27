# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sl(MakefilePackage):
    """SL: Cure your bad habit of mistyping"""

    homepage = "https://github.com/mtoyoda/sl"
    url = "https://github.com/mtoyoda/sl/archive/5.02.tar.gz"

    license("MIT")

    version("5.02", sha256="1e5996757f879c81f202a18ad8e982195cf51c41727d3fea4af01fdcbbb5563a")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CC=.*", "CC=cc")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("sl", prefix.bin)
