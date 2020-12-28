# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dbcsr(CMakePackage, CudaPackage):
    """Distributed Block Compressed Sparse Row matrix library."""

    homepage = "https://github.com/cp2k/dbcsr"
    git      = "https://github.com/cp2k/dbcsr.git"

    maintainers = ['dev-zero']

    version('develop', branch='develop')

    variant('mpi',    default=True,  description='Compile with MPI')
    variant('openmp', default=False, description='Build with OpenMP support')
    variant('shared', default=True,  description='Build shared library')
    variant('smm', default='libxsmm', values=('libxsmm', 'blas'),
            description='Library for small matrix multiplications')
    variant('cuda_arch',
            description='CUDA architecture',
            default='none',
            values=('none', '35', '37', '60', '70'),
            multi=False)
    variant('cuda_arch_35_k20x', default=False,
            description=('CP2K (resp. DBCSR) has specific parameter sets for'
                         ' different GPU models. Enable this when building'
                         ' with cuda_arch=35 for a K20x instead of a K40'))

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('libxsmm@1.11:~header-only', when='smm=libxsmm')

    depends_on('cmake@3.12:', type='build')
    depends_on('py-fypp', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@3.6:', type='build', when='+cuda')

    conflicts('+cuda', when='cuda_arch=none')

    generator = 'Ninja'
    depends_on('ninja@1.10:', type='build')

    def cmake_args(self):
        if ('+openmp' in self.spec
            and '^openblas' in self.spec
            and '^openblas threads=openmp' not in self.spec):
            raise InstallError(
                '^openblas threads=openmp required for dbcsr+openmp')

        spec = self.spec
        args = [
            '-DUSE_SMM=%s' % ('libxsmm' if 'smm=libxsmm' in spec else 'blas'),
            '-DUSE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
            '-DUSE_OPENMP=%s' % (
                'ON' if '+openmp' in spec else 'OFF'),
            # C API needs MPI
            '-DWITH_C_API=%s' % ('ON' if '+mpi' in spec else 'OFF'),
            '-DBLAS_FOUND=true',
            '-DBLAS_LIBRARIES=%s' % (spec['blas'].libs.joined(';')),
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES=%s' % (spec['lapack'].libs.joined(';')),
            '-DWITH_EXAMPLES=ON',
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if '+shared' in spec else 'OFF'),
        ]

        if '+cuda' in self.spec:
            cuda_arch = self.spec.variants['cuda_arch'].value

            gpuver = {
                '35': 'K40',
                '37': 'K80',
                '60': 'P100',
                '70': 'V100',
            }[cuda_arch]

            if (cuda_arch == '35'
                    and self.spec.satisfies('+cuda_arch_35_k20x')):
                gpuver = 'K20X'

            args += ['-DWITH_GPU=%s' % gpuver]

        return args

    def check(self):
        """Override CMakePackage's check() to enforce seralized test runs
           since they are already parallelized"""
        with working_dir(self.build_directory):
            self._if_ninja_target_execute('test', parallel=False)
