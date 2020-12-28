# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class SnapKorf(MakefilePackage):
    """SNAP is a general purpose gene finding program suitable for both
       eukaryotic and prokaryotic genomes."""

    homepage = "http://korflab.ucdavis.edu/software.html"
    url      = "http://korflab.ucdavis.edu/Software/snap-2013-11-29.tar.gz"

    version('2013-11-29', sha256='e2a236392d718376356fa743aa49a987aeacd660c6979cee67121e23aeffc66a')

    depends_on('perl', type=('build', 'run'))
    depends_on('boost')
    depends_on('sqlite')
    depends_on('sparsehash')

    conflicts('%gcc@5:', when='@2013-11-29')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        progs  = ['snap', 'fathom', 'forge', 'depend', 'exonpairs', 'hmm-info']
        for p in progs:
            install(p, prefix.bin)

        install('*.pl', prefix.bin)

        install_tree('Zoe', prefix.Zoe)
        install_tree('HMM', prefix.HMM)
        install_tree('DNA', prefix.DNA)

    def setup_run_environment(self, env):
        env.set('ZOE', self.prefix)
        env.prepend_path('PATH', self.prefix)
