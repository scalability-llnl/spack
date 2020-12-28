# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fraggenescan(MakefilePackage):
    """FragGeneScan is an application for finding (fragmented) genes in short
       reads. It can also be applied to predict prokaryotic genes in
       incomplete assemblies or complete genomes."""

    homepage = "https://sourceforge.net/projects/fraggenescan/"
    url      = "https://downloads.sourceforge.net/project/fraggenescan/FragGeneScan1.31.tar.gz"

    version('1.31', sha256='cd3212d0f148218eb3b17d24fcd1fc897fb9fee9b2c902682edde29f895f426c')

    build_targets = ['clean', 'hmm.obj']

    def edit(self, spec, prefix):
        filter_file('gcc', spack_cc, 'Makefile', string=True)

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
