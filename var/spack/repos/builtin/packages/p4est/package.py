# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class P4est(AutotoolsPackage):
    """Dynamic management of a collection (a forest) of adaptive octrees in
    parallel"""
    homepage = "https://www.p4est.org"
    url      = "https://github.com/cburstedde/p4est/archive/refs/tags/v2.3.1.tar.gz"

    maintainers = ['davydden']

    version('2.3.1', sha256='8acd592863f440656f8a97561f323b7e888fd82127203c06ae2e14753dea66a2')
    version('2.3',   sha256='3fa2471888e07152d77e002d216d109c0d8bbc144fe3fd89833845883e28d3b8')
    version('2.2',   sha256='7df0e9a161b6ea680324dfdbc0ffc6e0d0a6c9c9b0ea5b37c973e71a054226c2')
    version('2.1',   sha256='83938a46a016f1836e63b63800366b8c9906f246bc8340aaebb6e74fd9de590b')
    version('2.0',   sha256='1533989c089253372bf3a134740a06cad3fff6c6e9969c09dc31ee14b27f1efe')
    version('1.1',   sha256='14a4ba6c5883ece611c90fae29bc60a454c20db43df646b232bd5aa552acd5cf')

    variant('mpi', default=True, description='Enable MPI')
    variant('openmp', default=False, description='Enable OpenMP')

    # build dependencies
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool@2.4.2:', type='build')

    # other dependencies
    depends_on('mpi', when='+mpi')
    depends_on('zlib')

    # from sc upstream, correct the default libraries
    patch('https://github.com/cburstedde/libsc/commit/b506aab224b988fec210cc212469f2c4f58b2d04.patch',
          sha256='e9418b1a9347a409be241cd185519b31950e42a7f55b6fb80ce53097657098ee',
          working_dir='sc',
          when='@2.0')
    patch('https://github.com/cburstedde/libsc/commit/b45a51a7ef97883a3d4dcbd05cb2c77890a76f75.patch',
          sha256='8fb829e34e3a1e28afdd6e56e0bdc1d377af569b7ccb9e9d8da0eeb5829ed27e',
          working_dir='sc',
          when='@2.0')

    def autoreconf(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap()

    def configure_args(self):
        args = [
            '--enable-shared',
            '--disable-vtk-binary',
            '--without-blas',
            'CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL',
            'CFLAGS=-O2'
        ]

        if '~mpi' in self.spec:
            args.append('--disable-mpi')
        else:
            args.append('--enable-mpi')
            args.append('CC=%s'  % self.spec['mpi'].mpicc)
            args.append('CXX=%s' % self.spec['mpi'].mpicxx)
            args.append('FC=%s'  % self.spec['mpi'].mpifc)
            args.append('F77=%s' % self.spec['mpi'].mpif77)

        if '+openmp' in self.spec:
            try:
                args.append(
                    '--enable-openmp={0}'.format(self.compiler.openmp_flag))
            except UnsupportedCompilerFlag:
                args.append('--enable-openmp')
        else:
            args.append('--disable-openmp')

        return args
