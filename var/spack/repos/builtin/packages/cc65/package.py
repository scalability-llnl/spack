# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cc65(MakefilePackage):
    """cc65 is a complete cross development package for 65(C)02 systems,
    including a powerful macro assembler, a C compiler, linker, librarian
    and several other tools."""

    homepage = "https://cc65.github.io/"
    url = "https://github.com/cc65/cc65/archive/V2.18.tar.gz"

    license("Zlib")

    version("2.18", sha256="d14a22fb87c7bcbecd8a83d5362d5d317b19c6ce2433421f2512f28293a6eaab")
    version("2.17", sha256="73b89634655bfc6cef9aa0b8950f19657a902ee5ef0c045886e418bb116d2eac")
    version("2.16", sha256="fdbbf1efbf2324658a5774fdceef4a1b202322a04f895688d95694843df76792")
    version("2.15", sha256="adeac1a4b04183dd77fba1d69e56bbf4a6d358e0b253ee43ef4cac2391ba848a")
    version("2.14", sha256="128bda63490eb43ad25fd3615adee4c819c0b7da4b9b8f1801df36bd19e3bdf8")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
