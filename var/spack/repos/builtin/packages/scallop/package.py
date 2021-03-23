# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Scallop(AutotoolsPackage):
    """Scallop is a reference-based transcriptome assembler for RNA-seq"""

    homepage = "https://github.com/Kingsford-Group/scallop"
    url      = "https://github.com/Kingsford-Group/scallop/releases/download/v0.10.3/scallop-0.10.3.tar.gz"

    version('0.10.3', sha256='04eb3ab27ed8c7ae38e1780d6b2af16b6a2c01807ffafd59e819d33bfeff58a0')

    depends_on('clp')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('htslib@1.5:')

    def configure_args(self):
        return [
            '--with-clp={0}'.format(self.spec['clp'].prefix),
            '--with-htslib={0}'.format(self.spec['htslib'].prefix),
            '--with-boost={0}'.format(self.spec['boost'].prefix),
        ]
