# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amrex(CMakePackage, CudaPackage, ROCmPackage):
    """AMReX is a publicly available software framework designed
    for building massively parallel block- structured adaptive
    mesh refinement (AMR) applications."""

    homepage = "https://amrex-codes.github.io/amrex/"
    url      = "https://github.com/AMReX-Codes/amrex/releases/download/20.05/amrex-20.05.tar.gz"
    git      = "https://github.com/AMReX-Codes/amrex.git"

    maintainers = ['mic84', 'asalmgren']

    version('develop', branch='development')
    version('21.04', sha256='1c610e4b0800b16f7f1da74193ff11af0abfb12198b36a7e565a6a7f793087fa')
    version('21.03', sha256='6307bf75c80c2076bf5bd1cff4d12483280a32b5175fe117f32eed9c89cd1ac5')
    version('21.02', sha256='4a7ef997c43f9f03f1b06dd1aafa01218773a3265a5c1811f77eb4521b5e75b3')
    version('21.01', sha256='59de3ed429347ee6a7ad4f09c0c431248f2e081f59c301db37cacb36993622f4')
    version('20.12', sha256='a8ba1d605780250da77619939582ce44b33cd286f2dbcc0dfd5cdbaf209140a5')
    version('20.11', sha256='b86f4f2ebf414cec050e562d4ab81545944bda581b496d69767b4bf6a3060855')
    version('20.10', sha256='92def480d1f0bcb5bcb9dfae2ddc8997060414386a1d71ccbfdad785fa2e46fa')
    version('20.09', sha256='3ae203f18656117d8201da16e899a6144ec217817a2a5d9b7649e2eef9cacdf9')
    version('20.08', sha256='a202430cd8dbef2de29b20fe9b5881cc58ee762326556ec3c0ad9c3f85ddfc2f')
    version('20.07', sha256='c386f566f4c57ee56b5630f79ce2c6117d5a612a4aab69b7b26e48d577251165')
    version('20.06', sha256='be2f2a5107111fcb8b3928b76024b370c7cb01a9e5dd79484cf7fcf59d0b4858')
    version('20.05', sha256='97d753bb75e845a0a959ec1a044a48e6adb86dd008b5e29ce7a01d49ed276338')
    version('20.04', sha256='a7ece54d5d89cc00fd555551902a0d4d0fb50db15d2600f441353eed0dddd83b')
    version('20.03', sha256='9728f20c0d7297c935fe5cbc63c1ee60f983b833a735c797340ee2765d626165')
    version('20.02', sha256='2eda858b43e7455718ccb96c18f678da1778ec61031e90effdcb9c3e7e6f9bb5')
    version('20.01', sha256='957e7a7fe90a0a9f4ae10bf9e46dba68d72448d0bec69a4a4e66a544930caca3')
    version('19.10', sha256='9f30a2b3ec13711dfc6a1b59af59bd7df78449b5846ac6457b5dbbdecb20c576')
    version('19.08', sha256='94b1e9a9dcfb8c5b52aef91a2ed373aef504d766dd7d0aba6731ceb94e48e940')
    version('18.10.1', sha256='e648465c9c3b7ff4c696dfa8b6d079b4f61c80d96c51e27af210951c9367c201')
    version('18.10', sha256='298eba03ef03d617c346079433af1089d38076d6fab2c34476c687740c1f4234')
    version('18.09.1', sha256='a065ee4d1d98324b6c492ae20ea63ba12a4a4e23432bf5b3fe9788d44aa4398e')

    # Config options
    variant('dimensions', default='3',
            description='Dimensionality', values=('2', '3'))
    variant('shared',  default=False,
            description='Build shared library')
    variant('mpi',          default=True,
            description='Build with MPI support')
    variant('openmp',       default=False,
            description='Build with OpenMP support')
    variant('precision',  default='double',
            description='Real precision (double/single)',
            values=('single', 'double'))
    variant('eb',  default=False,
            description='Build Embedded Boundary classes')
    variant('fortran',  default=False,
            description='Build Fortran API')
    variant('linear_solvers', default=True,
            description='Build linear solvers')
    variant('amrdata',    default=False,
            description='Build data services')
    variant('particles',  default=False,
            description='Build particle classes')
    variant('sundials', default=False,
            description='Build AMReX with SUNDIALS support')
    variant('hdf5',  default=False,
            description='Enable HDF5-based I/O')
    variant('hypre', default=False,
            description='Enable Hypre interfaces')
    variant('petsc', default=False,
            description='Enable PETSc interfaces')
    variant('pic', default=False,
            description='Enable PIC')

    # Build dependencies
    depends_on('mpi', when='+mpi')
    depends_on('sundials@4.0.0:4.1.0 +ARKODE +CVODE', when='@19.08: +sundials')
    depends_on('cuda@9.0.0:', when='+cuda')
    depends_on('python@2.7:', type='build', when='@:20.04')
    depends_on('cmake@3.5:',  type='build', when='@:18.10.99')
    depends_on('cmake@3.13:', type='build', when='@18.11:')
    depends_on('cmake@3.14:', type='build', when='@19.04:')
    # cmake @3.17: is necessary to handle cuda @11: correctly
    depends_on('cmake@3.17:', type='build', when='^cuda @11:')
    depends_on('hdf5@1.10.4: +mpi', when='+hdf5')
    depends_on('rocrand', type='build', when='+rocm')
    depends_on('hypre@2.18.2:', type='link', when='@:21.02 +hypre')
    depends_on('hypre@2.19.0:', type='link', when='@21.03: ~cuda +hypre')
    depends_on('hypre@2.20.0:', type='link', when='@21.03: +cuda +hypre')
    depends_on('petsc', type='link', when='+petsc')

    # these versions of gcc have lambda function issues
    # see https://github.com/spack/spack/issues/22310
    conflicts('%gcc@8.1.0:8.3.0', when='@21.03')
    conflicts('%gcc@8.1.0:8.2.0', when='@21.01:21.02')

    # Check options compatibility
    conflicts('+sundials', when='~fortran',
              msg='AMReX SUNDIALS support needs AMReX Fortran API (+fortran)')
    conflicts('+sundials', when='@20.12:',
              msg='AMReX >= 20.12 no longer supports SUNDIALS interfaces')
    conflicts('+hdf5', when='@:20.06',
              msg='AMReX HDF5 support needs AMReX newer than version 20.06')
    conflicts('+hypre', when='@:20.06',
              msg='AMReX Hypre support needs AMReX newer than version 20.06')
    conflicts('+hypre', when='@:20.07 ~fortran',
              msg='AMReX < 20.08 needs the Fortran API (+fortran) for Hypre support')
    conflicts('+hypre', when='~linear_solvers',
              msg='AMReX Hypre support needs variant +linear_solvers')
    conflicts('+petsc', when='@:20.06',
              msg='PETSc support needs AMReX newer than version 20.06')
    conflicts('+petsc', when='@:20.07 ~fortran',
              msg='AMReX < 20.08 needs the Fortran API (+fortran) for PETSc support')
    conflicts('+petsc', when='~linear_solvers',
              msg='AMReX PETSc support needs variant +linear_solvers')
    conflicts('+cuda', when='@:19.08',
              msg='AMReX CUDA support needs AMReX newer than version 19.08')
    conflicts('cuda_arch=10', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=11', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=12', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=13', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=20', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=21', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=30', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('cuda_arch=32', when='+cuda', msg='AMReX only supports compute capabilities >= 3.5')
    conflicts('+rocm', when='@:20.11', msg='AMReX HIP support needs AMReX newer than version 20.11')
    conflicts('+cuda', when='+rocm', msg='CUDA and HIP support are exclusive')

    def url_for_version(self, version):
        if version >= Version('20.05'):
            url = "https://github.com/AMReX-Codes/amrex/releases/download/{0}/amrex-{0}.tar.gz"
        else:
            url = "https://github.com/AMReX-Codes/amrex/archive/{0}.tar.gz"
        return url.format(version.dotted)

    def get_cuda_arch_string(self, values):
        if 'none' in values:
            return 'Auto'
        else:
            # Use format x.y instead of CudaPackage xy format
            vf = tuple(float(x) / 10.0 for x in values)
            return ';'.join(str(x) for x in vf)

    #
    # For versions > 20.11
    #
    @when('@20.12:,develop')
    def cmake_args(self):
        args = [
            '-DUSE_XSDK_DEFAULTS=ON',
            self.define_from_variant('AMReX_SPACEDIM', 'dimensions'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('AMReX_MPI', 'mpi'),
            self.define_from_variant('AMReX_OMP', 'openmp'),
            '-DXSDK_PRECISION:STRING=%s' %
            self.spec.variants['precision'].value.upper(),
            self.define_from_variant('XSDK_ENABLE_Fortran', 'fortran'),
            self.define_from_variant('AMReX_FORTRAN_INTERFACES', 'fortran'),
            self.define_from_variant('AMReX_EB', 'eb'),
            self.define_from_variant('AMReX_LINEAR_SOLVERS',
                                     'linear_solvers'),
            self.define_from_variant('AMReX_AMRDATA', 'amrdata'),
            self.define_from_variant('AMReX_PARTICLES', 'particles'),
            self.define_from_variant('AMReX_HDF5', 'hdf5'),
            self.define_from_variant('AMReX_HYPRE', 'hypre'),
            self.define_from_variant('AMReX_PETSC', 'petsc'),
            self.define_from_variant('AMReX_PIC', 'pic'),
        ]

        if self.spec.satisfies('%fj'):
            args.append('-DCMAKE_Fortran_MODDIR_FLAG=-M')

        if '+cuda' in self.spec:
            args.append('-DAMReX_GPU_BACKEND=CUDA')
            args.append('-DAMReX_CUDA_ERROR_CAPTURE_THIS=ON')
            args.append('-DAMReX_CUDA_ERROR_CROSS_EXECUTION_SPACE_CALL=ON')
            cuda_arch = self.spec.variants['cuda_arch'].value
            args.append('-DAMReX_CUDA_ARCH=' + self.get_cuda_arch_string(cuda_arch))

        if '+rocm' in self.spec:
            args.append('-DCMAKE_CXX_COMPILER={0}'.format(self.spec['hip'].hipcc))
            args.append('-DAMReX_GPU_BACKEND=HIP')
            targets = self.spec.variants['amdgpu_target'].value
            args.append('-DAMReX_AMD_ARCH=' + ';'.join(str(x) for x in targets))

        return args

    #
    # For versions <= 20.11
    #
    @when('@:20.11')
    def cmake_args(self):
        args = [
            '-DUSE_XSDK_DEFAULTS=ON',
            self.define_from_variant('DIM', 'dimensions'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            '-DXSDK_PRECISION:STRING=%s' %
            self.spec.variants['precision'].value.upper(),
            self.define_from_variant('XSDK_ENABLE_Fortran', 'fortran'),
            self.define_from_variant('ENABLE_FORTRAN_INTERFACES', 'fortran'),
            self.define_from_variant('ENABLE_EB', 'eb'),
            self.define_from_variant('ENABLE_LINEAR_SOLVERS',
                                     'linear_solvers'),
            self.define_from_variant('ENABLE_AMRDATA', 'amrdata'),
            self.define_from_variant('ENABLE_PARTICLES', 'particles'),
            self.define_from_variant('ENABLE_SUNDIALS', 'sundials'),
            self.define_from_variant('ENABLE_HDF5', 'hdf5'),
            self.define_from_variant('ENABLE_HYPRE', 'hypre'),
            self.define_from_variant('ENABLE_PETSC', 'petsc'),
            self.define_from_variant('ENABLE_CUDA', 'cuda'),
        ]

        if self.spec.satisfies('%fj'):
            args.append('-DCMAKE_Fortran_MODDIR_FLAG=-M')

        if '+cuda' in self.spec:
            cuda_arch = self.spec.variants['cuda_arch'].value
            args.append('-DCUDA_ARCH=' + self.get_cuda_arch_string(cuda_arch))

        return args
