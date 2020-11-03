# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dihydrogen(CMakePackage, CudaPackage):
    """DiHydrogen is the second version of the Hydrogen fork of the
       well-known distributed linear algebra library,
       Elemental. DiHydrogen aims to be a basic distributed
       multilinear algebra interface with a particular emphasis on the
       needs of the distributed machine learning effort, LBANN."""

    homepage = "https://github.com/LLNL/DiHydrogen.git"
    url      = "https://github.com/LLNL/DiHydrogen/archive/v0.1.tar.gz"
    git      = "https://github.com/LLNL/DiHydrogen.git"

    maintainers = ['bvanessen']

    version('develop', branch='develop')
    version('master', branch='master')

    version('0.1', sha256='171d4b8adda1e501c38177ec966e6f11f8980bf71345e5f6d87d0a988fef4c4e')

    variant('al', default=True,
            description='Builds with Aluminum communication library')
    variant('developer', default=False,
            description='Enable extra warnings and force tests to be enabled.')
    variant('half', default=False,
            description='Enable FP16 support on the CPU.')
    variant('legacy', default=False,
            description='Enable the legacy DistConv code branch.')
    variant('nvshmem', default=False,
            description='Builds with support for NVSHMEM')
    variant('openmp', default=False,
            description='Enable CPU acceleration with OpenMP threads.')
    variant('rocm', default=False,
            description='Enable ROCm/HIP language features.')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('docs', default=False,
            description='Builds with support for building documentation')

    # Variants related to BLAS
    variant('openmp_blas', default=False,
            description='Use OpenMP for threading in the BLAS library')
    variant('int64_blas', default=False,
            description='Use 64bit integers for BLAS.')
    variant('blas', default='openblas', values=('openblas', 'mkl', 'accelerate', 'essl'),
            description='Enable the use of OpenBlas/MKL/Accelerate/ESSL')

    # Override the default set of CUDA architectures with the relevant
    # subset from lib/spack/spack/build_systems/cuda.py
    cuda_arch_values = [
        '30', '32', '35', '37',
        '50', '52', '53',
        '60', '61', '62',
        '70', '72', '75',
        '80'
    ]
    variant('cuda_arch',
            description='CUDA architecture',
            values=spack.variant.auto_or_any_combination_of(*cuda_arch_values))

    depends_on('mpi')
    depends_on('catch2', type='test')

    # Specify the correct version of Aluminum
    depends_on('aluminum@0.4:0.4.99', when='@0.1:0.1.99 +al')
    depends_on('aluminum@0.5:', when='@:0.0,0.2: +al')

    # Add Aluminum variants
    depends_on('aluminum +cuda +nccl +ht +cuda_rma', when='+al +cuda')

    depends_on('cuda', when=('+cuda' or '+legacy'))
    depends_on('cudnn', when=('+cuda' or '+legacy'))
    depends_on('cub', when='^cuda@:10.99')

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

    # Legacy builds require cuda
    conflicts('~cuda', when='+legacy')

    depends_on('half', when='+half')

    generator = 'Ninja'
    depends_on('ninja', type='build')
    depends_on('cmake@3.16.0:', type='build')

    depends_on('py-breathe', type='build', when='+docs')
    depends_on('doxygen', type='build', when='+docs')

    illegal_cuda_arch_values = [
        '10', '11', '12', '13',
        '20', '21',
    ]
    for value in illegal_cuda_arch_values:
        conflicts('cuda_arch=' + value)

    @property
    def libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libH2Core', root=self.prefix, shared=shared, recursive=True
        )

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
            '-DBUILD_SHARED_LIBS:BOOL=%s'      % ('+shared' in spec),
            '-DH2_ENABLE_CUDA=%s' % ('+cuda' in spec),
            '-DH2_ENABLE_DISTCONV_LEGACY=%s' % ('+legacy' in spec),
            '-DH2_ENABLE_OPENMP=%s' % ('+openmp' in spec),
            '-DH2_ENABLE_FP16=%s' % ('+half' in spec),
            '-DH2_ENABLE_HIP_ROCM=%s' % ('+rocm' in spec),
            '-DH2_DEVELOPER_BUILD=%s' % ('+developer' in spec),
        ]

        if '+cuda' in spec:
            cuda_arch = spec.variants['cuda_arch'].value
            if len(cuda_arch) == 1 and cuda_arch[0] == 'auto':
                args.append('-DCMAKE_CUDA_FLAGS=-arch=sm_60')
            else:
                cuda_arch = [x for x in spec.variants['cuda_arch'].value
                             if x != 'auto']
                if cuda_arch:
                    args.append('-DCMAKE_CUDA_FLAGS={0}'.format(
                        ' '.join(self.cuda_flags(cuda_arch))
                    ))

        return args
