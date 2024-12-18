# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bamdst(MakefilePackage):
    """Bamdst is a a lightweight bam file depth statistical tool."""

    homepage = "https://github.com/shiquan/bamdst"
    git = "https://github.com/shiquan/bamdst.git"

    version("master", git="https://github.com/shiquan/bamdst.git")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    parallel = False

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CC= .*", "CC = cc")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("bamdst", prefix.bin)
