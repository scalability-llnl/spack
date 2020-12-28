# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minife(MakefilePackage):
    """Proxy Application. MiniFE is an proxy application
       for unstructured implicit finite element codes.
    """

    homepage = "https://mantevo.org/"
    url      = "https://github.com/Mantevo/miniFE/archive/v2.1.0.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('2.1.0', sha256='59f4c56d73d2a758cba86939db2d36e12705282cb4174ce78223d984527f5d15')

    variant('build', default='ref', description='Type of Parallelism',
            values=('ref', 'openmp_ref', 'qthreads', 'kokkos'))

    depends_on('mpi')
    depends_on('qthreads', when='build=qthreads')

    @property
    def build_targets(self):
        targets = [
            '--directory={0}/src'.format(self.spec.variants['build'].value),
            'CXX={0}'.format(self.spec['mpi'].mpicxx),
            'CC={0}'.format(self.spec['mpi'].mpicc)
        ]

        return targets

    def edit(self, spec, prefix):
        makefile = FileFilter('{0}/src/Makefile'.format(
                              self.spec.variants['build'].value))

        makefile.filter('-fopenmp', self.compiler.openmp_flag, string=True)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('{0}/src/miniFE.x'.format(self.spec.variants['build'].value),
                prefix.bin)
