# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Masurca(Package):
    """MaSuRCA is whole genome assembly software. It combines the efficiency
       of the de Bruijn graph and Overlap-Layout-Consensus (OLC)
       approaches."""

    homepage = "http://www.genome.umd.edu/masurca.html"
    url = "https://github.com/alekseyzimin/masurca/releases/download/v3.3.1/MaSuRCA-3.3.1.tar.gz"

    version('4.0.1', sha256='68628acaf3681d09288b48a35fec7909b347b84494fb26c84051942256299870')
    version('3.3.1', sha256='587d0ee2c6b9fbd3436ca2a9001e19f251b677757fe5e88e7f94a0664231e020')
    version('3.2.9', sha256='795ad4bd42e15cf3ef2e5329aa7e4f2cdeb7e186ce2e350a45127e319db2904b')

    depends_on('perl', type=('build', 'run'))
    depends_on('boost')
    depends_on('zlib')
    patch('arm.patch', when='target=aarch64:')

    def patch(self):
        if self.spec.target.family == 'aarch64':
            for makefile in 'Makefile.am', 'Makefile.in':
                m = join_path('global-1', 'prepare', makefile)
                filter_file('-minline-all-stringops', '', m)
                m = join_path('global-1', makefile)
                filter_file('-minline-all-stringops', '', m)

    def setup_build_environment(self, env):
        if '@4:' in self.spec:
            env.set('DEST', self.prefix)

    def install(self, spec, prefix):
        installer = Executable('./install.sh')
        installer()
        if '@:4' in self.spec:
            install_tree('.', prefix)
