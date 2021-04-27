# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Dbcsr(CMakePackage, CudaPackage, ROCmPackage):
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
    variant('cuda_arch_35_k20x', default=False,
            description=('CP2K (resp. DBCSR) has specific parameter sets for'
                         ' different GPU models. Enable this when building'
                         ' with cuda_arch=35 for a K20x instead of a K40'))

    variant('opencl', default=False, description='Enable OpenCL backend')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('libxsmm@1.11:~header-only', when='smm=libxsmm')

    depends_on('cmake@3.12:', type='build')
    depends_on('py-fypp', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@3.6:', type='build', when='+cuda')

    depends_on('hipblas', when='+rocm')

    depends_on('opencl', when='+opencl')

    # We only support specific gpu archs for which we have parameter files
    # for optimal kernels. Note that we don't override the parent class arch
    # properties, since the parent class defines constraints for different archs
    # Instead just mark all unsupported cuda archs as conflicting.
    dbcsr_cuda_archs = ('35', '37', '60', '70')
    cuda_msg = 'dbcsr only supports cuda_arch {0}'.format(dbcsr_cuda_archs)

    for arch in CudaPackage.cuda_arch_values:
        if arch not in dbcsr_cuda_archs:
            conflicts('+cuda', when='cuda_arch={0}'.format(arch), msg=cuda_msg)

    conflicts('+cuda', when='cuda_arch=none', msg=cuda_msg)

    dbcsr_amdgpu_targets = ('gfx906')
    amd_msg = 'DBCSR only supports amdgpu_target {0}'.format(dbcsr_amdgpu_targets)

    for arch in ROCmPackage.amdgpu_targets:
        if arch not in dbcsr_amdgpu_targets:
            conflicts('+rocm', when='amdgpu_target={0}'.format(arch), msg=amd_msg)

    accel_msg = "CUDA, ROCm and OpenCL support are mutually exlusive"
    conflicts('+cuda', when='+rocm', msg=accel_msg)
    conflicts('+cuda', when='+opencl', msg=accel_msg)
    conflicts('+rocm', when='+opencl', msg=accel_msg)

    # Require openmp threading for OpenBLAS by making other options conflict
    conflicts('^openblas threads=pthreads', when='+openmp')
    conflicts('^openblas threads=none', when='+openmp')

    conflicts('smm=blas', when='+opencl')

    generator = 'Ninja'
    depends_on('ninja@1.10:', type='build')

    def cmake_args(self):
        spec = self.spec

        if len(spec.variants['cuda_arch'].value) > 1:
            raise InstallError("dbcsr supports only one cuda_arch at a time")

        if len(spec.variants['amdgpu_target'].value) > 1:
            raise InstallError("DBCSR supports only one amdgpu_arch at a time")

        args = [
            '-DUSE_SMM=%s' % ('libxsmm' if 'smm=libxsmm' in spec else 'blas'),
            self.define_from_variant('USE_MPI', 'mpi'),
            self.define_from_variant('USE_OPENMP', 'openmp'),
            # C API needs MPI
            self.define_from_variant('WITH_C_API', 'mpi'),
            '-DBLAS_FOUND=true',
            '-DBLAS_LIBRARIES=%s' % (spec['blas'].libs.joined(';')),
            '-DLAPACK_FOUND=true',
            '-DLAPACK_LIBRARIES=%s' % (spec['lapack'].libs.joined(';')),
            '-DWITH_EXAMPLES=ON',
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
        ]

        if self.spec.satisfies('+cuda'):
            cuda_arch = self.spec.variants['cuda_arch'].value[0]

            gpuver = {
                '35': 'K40',
                '37': 'K80',
                '60': 'P100',
                '70': 'V100',
            }[cuda_arch]

            if (cuda_arch == '35'
                    and self.spec.satisfies('+cuda_arch_35_k20x')):
                gpuver = 'K20X'

            args += [
                '-DWITH_GPU=%s' % gpuver,
                '-DUSE_ACCEL=cuda'
            ]

        if self.spec.satisfies('+rocm'):
            amd_arch = self.spec.variants['amdgpu_target'].value[0]

            gpuver = {
                'gfx906': 'Mi50'
            }[amd_arch]

            args += [
                '-DWITH_GPU={0}'.format(gpuver),
                '-DUSE_ACCEL=hip'
            ]

        if self.spec.satisfies('+opencl'):
            args += [
                '-DUSE_ACCEL=opencl'
            ]

        return args

    def check(self):
        """Override CMakePackage's check() to enforce seralized test runs
           since they are already parallelized"""
        with working_dir(self.build_directory):
            self._if_ninja_target_execute('test', parallel=False)
