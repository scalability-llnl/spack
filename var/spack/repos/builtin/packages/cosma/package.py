# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cosma(CMakePackage, CudaPackage):
    """
    Distributed Communication-Optimal Matrix-Matrix Multiplication Library
    """

    maintainers = ['haampie', 'kabicm', 'teonnik']
    homepage = 'https://github.com/eth-cscs/COSMA'
    url = 'https://github.com/eth-cscs/COSMA/releases/download/v2.2.0/cosma.tar.gz'
    git = 'https://github.com/eth-cscs/COSMA.git'

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version('master', branch='master', submodules=True)
    version('2.2.0', sha256='1eb92a98110df595070a12193b9221eecf9d103ced8836c960f6c79a2bd553ca')
    version('2.0.7', sha256='8d70bfcbda6239b6a8fbeaca138790bbe58c0c3aa576879480d2632d4936cf7e')
    version('2.0.2', sha256='4f3354828bc718f3eef2f0098c3bdca3499297497a220da32db1acd57920c68d')

    variant('scalapack', default=False,
            description='Build with ScaLAPACK API.')

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi@3:')
    depends_on('blas', when='~cuda')
    depends_on('scalapack', when='+scalapack')

    def setup_build_environment(self, env):
        if '+cuda' in self.spec:
            env.set('CUDA_PATH', self.spec['cuda'].prefix)

    def cmake_args(self):
        spec = self.spec
        args = ['-DCOSMA_WITH_TESTS=OFF',
                '-DCOSMA_WITH_APPS=OFF',
                '-DCOSMA_WITH_PROFILING=OFF',
                '-DCOSMA_WITH_BENCHMARKS=OFF']

        if '^mkl' in spec:
            args += ['-DCOSMA_BLAS=MKL']
        elif '^cray-libsci' in spec:
            args += ['-DCOSMA_BLAS=CRAY_LIBSCI']
        elif '^netlib-lapack' in spec:
            args += ['-DCOSMA_BLAS=CUSTOM']
        elif '^openblas' in spec:
            args += ['-DCOSMA_BLAS=OPENBLAS']
        elif '+cuda' in spec:
            args += ['-DCOSMA_BLAS=CUDA']
        else:  # TODO '^rocm' in spec:
            args += ['-DCOSMA_BLAS=ROCM']

        if '+scalapack' and '^mkl' in spec:
            args += ['-DCOSMA_SCALAPACK=MKL']
        elif '+scalapack' and '^cray-libsci' in spec:
            args += ['-DCOSMA_SCALAPACK=CRAY_LIBSCI']
        elif '+scalapack' and '^netlib-scalapack' in spec:
            args += ['-DCOSMA_SCALAPACK=CUSTOM']

        return args
