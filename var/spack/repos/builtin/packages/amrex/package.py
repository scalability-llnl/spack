# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amrex(CMakePackage):
    """AMReX is a publicly available software framework designed
    for building massively parallel block- structured adaptive
    mesh refinement (AMR) applications."""

    homepage = "https://amrex-codes.github.io/amrex/"
    url      = "https://github.com/AMReX-Codes/amrex/releases/download/20.05/amrex-20.05.tar.gz"
    git      = "https://github.com/AMReX-Codes/amrex.git"

    maintainers = ['mic84', 'asalmgren']

    version('develop', branch='development')
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
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('sundials', default=False,
            description='Build AMReX with SUNDIALS support')
    variant('hdf5',  default=False,
            description='Enable HDF5-based I/O')
    variant('hypre', default=False,
            description='Enable Hypre interfaces')
    variant('petsc', default=False,
            description='Enable PETSc interfaces')
    variant('cuda', default=False,
            description='Enable CUDA interfaces')

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
    conflicts('%apple-clang')
    conflicts('%clang')

    # Check options compatibility
    conflicts('+sundials', when='~fortran',
              msg='AMReX SUNDIALS support needs AMReX Fortran API (+fortran)')
    conflicts('+sundials', when='@20.12:',
              msg='AMReX >= 20.12 no longer supports SUNDIALS interfaces')
    conflicts('+hdf5', when='@:20.06',
              msg='AMReX HDF5 support needs AMReX newer than version 20.06')
    conflicts('+hypre', when='@:20.06',
              msg='AMReX Hypre support needs AMReX newer than version 20.06')
    conflicts('+hypre', when='~fortran',
              msg='AMReX Hypre support needs AMReX Fortran API (+fortran)')
    conflicts('+hypre', when='~linear_solvers',
              msg='AMReX Hypre support needs variant +linear_solvers')
    conflicts('+petsc', when='@:20.06',
              msg='AMReX PETSc support needs AMReX newer than version 20.06')
    conflicts('+petsc', when='~fortran',
              msg='AMReX PETSc support needs AMReX Fortran API (+fortran)')
    conflicts('+petsc', when='~linear_solvers',
              msg='AMReX PETSc support needs variant +linear_solvers')

    def url_for_version(self, version):
        if version >= Version('20.05'):
            url = "https://github.com/AMReX-Codes/amrex/releases/download/{0}/amrex-{0}.tar.gz"
        else:
            url = "https://github.com/AMReX-Codes/amrex/archive/{0}.tar.gz"
        return url.format(version.dotted)

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

        return args

    #
    # For versions > 20.11
    #
    @when('@20.12:')
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
            self.define_from_variant('AMReX_CUDA', 'cuda'),
        ]
        if self.spec.satisfies('%fj'):
            args.append('-DCMAKE_Fortran_MODDIR_FLAG=-M')

        return args
