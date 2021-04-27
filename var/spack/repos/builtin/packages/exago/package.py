# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exago(CMakePackage, CudaPackage):
    """ExaGO is a package for solving large-scale power grid optimization
    problems on parallel and distributed architectures, particularly targeted
    for exascale machines."""

    homepage = 'https://gitlab.pnnl.gov/exasgd/frameworks/exago'
    git = 'https://gitlab.pnnl.gov/exasgd/frameworks/exago.git'

    version('1.0.0', tag='v1.0.0')
    version('0.99.2', tag='v0.99.2')
    version('0.99.1', tag='v0.99.1')
    version('master', branch='master')
    version('develop', branch='develop')

    # Progrmming model options
    variant('mpi', default=True, description='Enable/Disable MPI')
    variant('raja', default=False, description='Enable/Disable RAJA')

    # Solver options
    variant('hiop', default=False, description='Enable/Disable HiOp')
    variant('petsc', default=True, description='Enable/Disable PETSc')
    variant('ipopt', default=False, description='Enable/Disable IPOPT')

    # Dependencides
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('cuda', when='+cuda')
    depends_on('raja', when='+raja')
    depends_on('raja+cuda', when='+raja+cuda')
    depends_on('umpire', when='+raja')

    # Some allocator code in Umpire only works with static libs
    depends_on('umpire+cuda~shared', when='+raja+cuda')

    # For some versions of RAJA package, camp cuda variant does not get set
    # correctly, so we must explicitly depend on it even though we don't use
    # camp
    depends_on('camp+cuda', when='+cuda')

    depends_on('cmake@3.18:', type='build')

    # HiOp dependency logic
    depends_on('hiop+shared', when='+hiop')
    depends_on('hiop+raja', when='+hiop+raja')
    depends_on('hiop@0.3.99:', when='@0.99:+hiop')
    depends_on('hiop+cuda', when='+hiop+cuda')
    depends_on('hiop~mpi', when='+hiop~mpi')
    depends_on('hiop+mpi', when='+hiop+mpi')

    depends_on('petsc', when='+petsc')
    depends_on('petsc~mpi', when='+petsc~mpi')
    depends_on('ipopt', when='+ipopt')

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append("-DEXAGO_RUN_TESTS=ON")

        args.append(self.define_from_variant('EXAGO_ENABLE_MPI', 'mpi'))
        args.append(self.define_from_variant('EXAGO_ENABLE_RAJA', 'raja'))
        args.append(self.define_from_variant('EXAGO_ENABLE_HIOP', 'hiop'))
        args.append(self.define_from_variant('EXAGO_ENABLE_PETSC', 'petsc'))
        args.append(self.define_from_variant('EXAGO_ENABLE_IPOPT', 'ipopt'))
        args.append(self.define_from_variant('EXAGO_ENABLE_GPU', 'cuda'))
        args.append(self.define_from_variant('EXAGO_ENABLE_CUDA', 'cuda'))

        if '+cuda' in spec:
            cuda_arch_list = spec.variants['cuda_arch'].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != 'none':
                args.append(
                    "-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch))

        if '+petsc' in spec:
            args.append("-DPETSC_DIR='{0}'".format(spec['petsc'].prefix))

        return args
