# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scallop(AutotoolsPackage):
    """Scallop is a reference-based transcriptome assembler for RNA-seq"""

    homepage = "https://github.com/Kingsford-Group/scallop"
    url      = "https://github.com/Kingsford-Group/scallop/releases/download/v0.10.3/scallop-0.10.3.tar.gz"

    version('0.10.3', sha256='04eb3ab27ed8c7ae38e1780d6b2af16b6a2c01807ffafd59e819d33bfeff58a0')

    depends_on('clp')
    depends_on('boost')
    depends_on('htslib@1.5:')

    def configure_args(self):
        return [
            '--with-clp={0}'.format(self.spec['clp'].prefix),
            '--with-htslib={0}'.format(self.spec['htslib'].prefix),
            '--with-boost={0}'.format(self.spec['boost'].prefix),
        ]
