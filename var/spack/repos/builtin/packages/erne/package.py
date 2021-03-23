# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Erne(AutotoolsPackage):
    """The Extended Randomized Numerical alignEr using BWT"""

    homepage = "http://erne.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/erne/2.1.1/erne-2.1.1-source.tar.gz"

    version('2.1.1', sha256='f32ab48481fd6c129b0a0246ab02b6e3a2a9da84024e1349510a59c15425d983')

    variant('mpi', default=False,
            description='Build with OpenMPI support')

    depends_on('boost@1.40.0:', type=('build', 'link', 'run'))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=('build', 'link', 'run'))
    depends_on('openmpi', type=('build', 'run'), when='+mpi')

    def configure_args(self):
        if '+mpi' in self.spec:
            return ['--enable-openmpi']
        else:
            return ['--disable-openmpi']

    def build(self, spec, prefix):
        # override the AUTOCONF environment to prevent double configure
        # this catches any invocations and ignores them
        make('AUTOCONF=:')

    def install(self, spec, prefix):
        # same catch with installing
        make('install', 'AUTOCONF=:')
