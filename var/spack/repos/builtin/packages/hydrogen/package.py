# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Hydrogen(CMakePackage, CudaPackage):
    """Hydrogen: Distributed-memory dense and sparse-direct linear algebra
       and optimization library. Based on the Elemental library."""

    homepage = "http://libelemental.org"
    url      = "https://github.com/LLNL/Elemental/archive/v1.0.1.tar.gz"
    git      = "https://github.com/LLNL/Elemental.git"

    maintainers = ['bvanessen']

    version('develop', branch='hydrogen')
    version('1.5.0', sha256='03dd487fb23b9fdbc715554a8ea48c3196a1021502e61b0172ef3fdfbee75180')
    version('1.4.0', sha256='c13374ff4a6c4d1076e47ba8c8d91a7082588b9958d1ed89cffb12f1d2e1452e')
    version('1.3.4', sha256='7979f6656f698f0bbad6798b39d4b569835b3013ff548d98089fce7c283c6741')
    version('1.3.3', sha256='a51a1cfd40ac74d10923dfce35c2c04a3082477683f6b35e7b558ea9f4bb6d51')
    version('1.3.2', sha256='50bc5e87955f8130003d04dfd9dcad63107e92b82704f8107baf95b0ccf98ed6')
    version('1.3.1', sha256='a8b8521458e9e747f2b24af87c4c2749a06e500019c383e0cefb33e5df6aaa1d')
    version('1.3.0', sha256='0f3006aa1d8235ecdd621e7344c99f56651c6836c2e1bc0cf006331b70126b36')
    version('1.2.0',   sha256='8545975139582ee7bfe5d00f8d83a8697afc285bf7026b0761e9943355974806')
    version('1.1.0-1', sha256='73ce05e4166853a186469269cb00a454de71e126b2019f95bbae703b65606808')
    version('1.1.0', sha256='b4c12913acd01c72d31f4522266bfeb8df1d4d3b4aef02e07ccbc9a477894e71')
    version('1.0.1', sha256='27cf76e1ef1d58bd8f9b1e34081a14a682b7ff082fb5d1da56713e5e0040e528')
    version('1.0', sha256='d8a97de3133f2c6b6bb4b80d32b4a4cc25eb25e0df4f0cec0f8cb19bf34ece98')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('hybrid', default=True,
            description='Make use of OpenMP within MPI packing/unpacking')
    variant('openmp_blas', default=False,
            description='Use OpenMP for threading in the BLAS library')
    variant('quad', default=False,
            description='Enable quad precision')
    variant('int64', default=False,
            description='Use 64bit integers')
    variant('int64_blas', default=False,
            description='Use 64bit integers for BLAS.')
    variant('scalapack', default=False,
            description='Build with ScaLAPACK library')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('blas', default='openblas', values=('openblas', 'mkl', 'accelerate', 'essl'),
            description='Enable the use of OpenBlas/MKL/Accelerate/ESSL')
    variant('mpfr', default=False,
            description='Support GNU MPFR\'s'
            'arbitrary-precision floating-point arithmetic')
    variant('cuda', default=False,
            description='Builds with support for GPUs via CUDA and cuDNN')
    variant('test', default=False,
            description='Builds test suite')
    variant('al', default=False,
            description='Builds with Aluminum communication library')
    variant('omp_taskloops', default=False,
            description='Use OpenMP taskloops instead of parallel for loops.')
    variant('half', default=True,
            description='Builds with support for FP16 precision data types')
    depends_on('cmake@3.16.0:', type='build')
    depends_on('mpi')
    depends_on('hwloc@2.0:')

    # Note that #1712 forces us to enumerate the different blas variants
    depends_on('openblas', when='blas=openblas ~openmp_blas ~int64_blas')
    depends_on('openblas +ilp64', when='blas=openblas ~openmp_blas +int64_blas')
    depends_on('openblas threads=openmp', when='blas=openblas +openmp_blas ~int64_blas')
    depends_on('openblas threads=openmp +lip64', when='blas=openblas +openmp_blas +int64_blas')

    depends_on('intel-mkl', when="blas=mkl ~openmp_blas ~int64_blas")
    depends_on('intel-mkl +ilp64', when="blas=mkl ~openmp_blas +int64_blas")
    depends_on('intel-mkl threads=openmp', when='blas=mkl +openmp_blas ~int64_blas')
    depends_on('intel-mkl@2017.1 +openmp +ilp64', when='blas=mkl +openmp_blas +int64_blas')

    depends_on('veclibfort', when='blas=accelerate')
    conflicts('blas=accelerate +openmp_blas')

    depends_on('essl -cuda', when='blas=essl -openmp_blas ~int64_blas')
    depends_on('essl -cuda +ilp64', when='blas=essl -openmp_blas +int64_blas')
    depends_on('essl threads=openmp', when='blas=essl +openmp_blas ~int64_blas')
    depends_on('essl threads=openmp +ilp64', when='blas=essl +openmp_blas +int64_blas')
    depends_on('netlib-lapack +external-blas', when='blas=essl')

    # Specify the correct version of Aluminum
    depends_on('aluminum@:0.3.99', when='@:1.3.99 +al')
    depends_on('aluminum@0.4:0.4.99', when='@1.4:1.4.99 +al')
    depends_on('aluminum@0.5:', when='@:1.0,1.5.0: +al')

    # Add Aluminum variants
    depends_on('aluminum +cuda +nccl +ht +cuda_rma', when='+al +cuda')

    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on('lapack', when='blas=openblas ~openmp_blas')

    depends_on('scalapack', when='+scalapack')
    depends_on('gmp', when='+mpfr')
    depends_on('mpc', when='+mpfr')
    depends_on('mpfr', when='+mpfr')

    depends_on('cuda', when='+cuda')
    depends_on('cub', when='^cuda@:10.99')
    depends_on('half', when='+half')

    conflicts('@0:0.98', msg="Hydrogen did not exist before v0.99. " +
              "Did you mean to use Elemental instead?")

    generator = 'Ninja'
    depends_on('ninja', type='build')

    @property
    def libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libEl', root=self.prefix, shared=shared, recursive=True
        )

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
            '-DBUILD_SHARED_LIBS:BOOL=%s'      % ('+shared' in spec),
            '-DHydrogen_ENABLE_OPENMP:BOOL=%s'       % ('+hybrid' in spec),
            '-DHydrogen_ENABLE_QUADMATH:BOOL=%s'     % ('+quad' in spec),
            '-DHydrogen_USE_64BIT_INTS:BOOL=%s'      % ('+int64' in spec),
            '-DHydrogen_USE_64BIT_BLAS_INTS:BOOL=%s' % ('+int64_blas' in spec),
            '-DHydrogen_ENABLE_MPC:BOOL=%s'        % ('+mpfr' in spec),
            '-DHydrogen_GENERAL_LAPACK_FALLBACK=ON',
            '-DHydrogen_ENABLE_ALUMINUM=%s' % ('+al' in spec),
            '-DHydrogen_ENABLE_CUB=%s' % ('+cuda' in spec),
            '-DHydrogen_ENABLE_CUDA=%s' % ('+cuda' in spec),
            '-DHydrogen_ENABLE_TESTING=%s' % ('+test' in spec),
            '-DHydrogen_ENABLE_HALF=%s' % ('+half' in spec),
        ]

        # Add support for OS X to find OpenMP (LLVM installed via brew)
        if self.spec.satisfies('%clang platform=darwin'):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args.extend([
                '-DOpenMP_DIR={0}'.format(clang_root)])

        if 'blas=openblas' in spec:
            args.extend([
                '-DHydrogen_USE_OpenBLAS:BOOL=%s' % ('blas=openblas' in spec),
                '-DOpenBLAS_DIR:STRING={0}'.format(
                    spec['openblas'].prefix)])
        elif 'blas=mkl' in spec:
            args.extend([
                '-DHydrogen_USE_MKL:BOOL=%s' % ('blas=mkl' in spec)])
        elif 'blas=accelerate' in spec:
            args.extend(['-DHydrogen_USE_ACCELERATE:BOOL=TRUE'])
        elif 'blas=essl' in spec:
            args.extend([
                '-DHydrogen_USE_ESSL:BOOL=%s' % ('blas=essl' in spec)])

        if '+omp_taskloops' in spec:
            args.extend([
                '-DHydrogen_ENABLE_OMP_TASKLOOP:BOOL=%s' %
                ('+omp_taskloops' in spec)])

        if '+al' in spec:
            args.extend([
                '-DHydrogen_ENABLE_ALUMINUM:BOOL=%s' % ('+al' in spec),
                '-DALUMINUM_DIR={0}'.format(
                    spec['aluminum'].prefix)])

        return args
