# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ecos(MakefilePackage):
    """A lightweight conic solver for second-order cone programming."""

    homepage = "https://github.com/embotech/ecos"
    url = "https://github.com/embotech/ecos/archive/2.0.7.tar.gz"

    license("GPL-3.0-only")

    version("2.0.7", sha256="bdb6a84f7d150820459bd0a796cb64ffbb019afb95dc456d22acc2dafb2e70e0")

    depends_on("c", type="build")  # generated

    build_targets = ["all", "shared"]

    def install(self, spec, prefix):
        install_tree("include", prefix.include)

        mkdir(prefix.lib)
        install("libecos.a", prefix.lib)
        install("libecos_bb.a", prefix.lib)
        install("libecos.so", prefix.lib)

        mkdir(prefix.bin)
        install("runecos", prefix.bin)
        install("runecosexp", prefix.bin)
