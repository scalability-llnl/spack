# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fraggenescan(MakefilePackage):
    """FragGeneScan is an application for finding (fragmented) genes in short
    reads. It can also be applied to predict prokaryotic genes in
    incomplete assemblies or complete genomes."""

    homepage = "https://sourceforge.net/projects/fraggenescan/"
    url = "https://downloads.sourceforge.net/project/fraggenescan/FragGeneScan1.31.tar.gz"

    version("1.31", sha256="cd3212d0f148218eb3b17d24fcd1fc897fb9fee9b2c902682edde29f895f426c")
    version("1.30", sha256="f2d7f0dfa4a5f4bbea295ed865dcbfedf16c954ea1534c2a879ebdcfb8650d95")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        filter_file("gcc", spack_cc, "Makefile", string=True)

    def build(self, spec, prefic):
        make("clean")
        make("fgs")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
