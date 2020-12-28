# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Seqtk(Package):
    """Toolkit for processing sequences in FASTA/Q formats."""

    homepage = "https://github.com/lh3/seqtk"
    url      = "https://github.com/lh3/seqtk/archive/v1.1.tar.gz"

    version('1.3', sha256='5a1687d65690f2f7fa3f998d47c3c5037e792f17ce119dab52fff3cfdca1e563')
    version('1.2', sha256='bd53316645ab10f0aaba59e1e72c28442ee4c9c37fddaacce5e24757eff78d7b')
    version('1.1', sha256='f01b9f9af6e443673a0105a7536a01957a4fc371826385a1f3dd1e417aa91d52')

    depends_on('zlib')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install('seqtk', prefix.bin)
        set_executable(join_path(prefix.bin, 'seqtk'))
