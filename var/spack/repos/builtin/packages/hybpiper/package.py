# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hybpiper(Package):
    """HybPiper was designed for targeted sequence capture, in which DNA
       sequencing libraries are enriched for gene regions of interest,
       especially for phylogenetics. HybPiper is a suite of Python scripts
       that wrap and connect bioinformatics tools in order to extract target
       sequences from high-throughput DNA sequencing reads"""

    homepage = "https://github.com/mossmatters/HybPiper"
    url      = "https://github.com/mossmatters/HybPiper/archive/v1.2.0.tar.gz"
    git      = "https://github.com/mossmatters/HybPiper/HybPiper.git"

    version('1.3.1', sha256='7ca07a9390d1ca52c72721774fa220546f18d3fa3b58500f68f3b2d89dbc0ecf')
    version('1.2.0', sha256='34c7b324e9bcacb6ccfe87dc50615d6f93866433b61a59291707efa858b6df57')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-biopython', type=('build', 'run'))
    depends_on('exonerate')
    depends_on('blast-plus')
    depends_on('spades')
    depends_on('parallel')
    depends_on('bwa')
    depends_on('samtools')

    def setup_run_environment(self, env):
        env.set('HYBPIPER_HOME', self.prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('*.py', prefix.bin)
