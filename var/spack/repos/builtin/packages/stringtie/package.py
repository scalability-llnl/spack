# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stringtie(MakefilePackage):
    """StringTie is a fast and highly efficient assembler of RNA-Seq alignments
       into potential transcripts."""

    homepage = "https://ccb.jhu.edu/software/stringtie"
    url      = "https://github.com/gpertea/stringtie/archive/v1.3.3b.tar.gz"

    version('1.3.4d', sha256='0134c0adc264efd31a1df4301b33bfcf3b3fe96bd3990ce3df90819bad9af968')
    version('1.3.4a', sha256='6164a5fa9bf8807ef68ec89f47e3a61fe57fa07fe858f52fb6627f705bf71add')
    version('1.3.3b', sha256='30e8a3a29b474f0abeef1540d9b4624a827d8b29d7347226d86a38afea28bc0f')

    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('stringtie', prefix.bin)
