# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys


class Sundials(CMakePackage, CudaPackage, ROCmPackage):
    """SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
    Solvers)"""

    homepage = "https://computing.llnl.gov/projects/sundials"
    urls = ["https://computing.llnl.gov/projects/sundials/download/sundials-2.7.0.tar.gz",
            "https://github.com/LLNL/sundials/releases/download/v2.7.0/sundials-2.7.0.tar.gz"]
    git = "https://github.com/llnl/sundials.git"
    maintainers = ['cswoodward', 'gardner48', 'balos1']

    # ==========================================================================
    # Versions
    # ==========================================================================
    version('develop', branch='develop')
    version('5.7.0', sha256='8d6dd094feccbb8d6ecc41340ec16a65fabac82ed4415023f6d7c1c2390ea2f3')
    version('5.6.1', sha256='16b77999ec7e7f2157aa1d04ca1de4a2371ca8150e056d24951d0c58966f2a83')
    version('5.6.0', sha256='95e4201912e150f29c6f6f7625de763385e2073dae7f929c4a544561ea29915d')
    version('5.5.0', sha256='2a755e89aab96d2ff096a4e30bf00bb162e80be20e9e99f424dccfb249098237')
    version('5.4.0', sha256='04d8a2ebe02cdaeef5a9e22ff7e3146bb563d8400f65772b6c7af80001413ffa')
    version('5.3.0', sha256='88dff7e11a366853d8afd5de05bf197a8129a804d9d4461fb64297f1ef89bca7')
    version('5.2.0', sha256='95f058acce5bd66e654de65acdbb1c9f44c90cf1b4e28f8d933cdb4415ebba3e')
    version('5.1.0', sha256='fb22d14fad42203809dc46d046b001149ec4e901b23882bd4a80619157fd9b21')
    version('5.0.0', sha256='345141ec01c641d0bdfb3476c478b7e74fd6a7192a478a27cafe75d9da2d7dd3')
    version('4.1.0', sha256='280de1c27b2360170a6f46cb3799b2aee9dff3bddbafc8b08c291a47ab258aa5')
    version('4.0.1', sha256='29e409c8620e803990edbda1ebf49e03a38c08b9187b90658d86bddae913aed4')
    version('3.2.1', sha256='47d94d977ab2382cdcdd02f72a25ebd4ba8ca2634bbb2f191fe1636e71c86808')
    version('3.2.0', sha256='d2b690afecadf8b5a048bb27ab341de591d714605b98d3518985dfc2250e93f9')
    version('3.1.2', sha256='a8985bb1e851d90e24260450667b134bc13d71f5c6effc9e1d7183bd874fe116')
    version('3.1.1', sha256='a24d643d31ed1f31a25b102a1e1759508ce84b1e4739425ad0e18106ab471a24')
    version('3.1.0', sha256='18d52f8f329626f77b99b8bf91e05b7d16b49fde2483d3a0ea55496ce4cdd43a')
    version('3.0.0', sha256='28b8e07eecfdef66e2c0d0ea0cb1b91af6e4e94d71008abfe80c27bf39f63fde')
    version('2.7.0', sha256='d39fcac7175d701398e4eb209f7e92a5b30a78358d4a0c0fcc23db23c11ba104')
    version('2.6.2', sha256='d8ed0151509dd2b0f317b318a4175f8b95a174340fc3080b8c20617da8aa4d2f')

    # ==========================================================================
    # Variants
    # ==========================================================================

    # SUNDIALS solvers
    sun_solvers = ['CVODE', 'CVODES', 'ARKODE', 'IDA', 'IDAS', 'KINSOL']

    for pkg in sun_solvers:
        variant(pkg, default=True,
                description='Enable %s solver' % pkg)

    # Real type
    variant(
        'precision',
        default='double',
        description='real type precision',
        values=('single', 'double', 'extended'),
        multi=False
    )

    # Index type
    variant('int64', default=False,
            description='Use 64bit integers for indices')

    # Parallelism
    variant('mpi',     default=True,
            description='Enable MPI parallel vector')
    variant('openmp',  default=False,
            description='Enable OpenMP parallel vector')
    variant('pthread', default=False,
            description='Enable Pthreads parallel vector')
    variant('raja',    default=False,
            description='Enable RAJA vector')

    # External libraries
    variant('hypre',        default=False,
            description='Enable Hypre MPI parallel vector')
    variant('lapack',       default=False,
            description='Enable LAPACK direct solvers')
    variant('klu',          default=False,
            description='Enable KLU sparse, direct solver')
    variant('petsc',        default=False,
            description='Enable PETSc interfaces')
    variant('superlu-mt',   default=False,
            description='Enable SuperLU_MT sparse, direct solver')
    variant('superlu-dist', default=False,
            description='Enable SuperLU_DIST sparse, direct solver')
    variant('trilinos', default=False,
            description='Enable Trilinos interfaces')

    # Library type
    variant('shared', default=True,
            description='Build shared libraries')
    variant('static', default=True,
            description='Build static libraries')

    # Fortran interfaces
    variant('fcmix', default=False,
            description='Enable Fortran 77 interface')
    variant('f2003', default=False,
            description='Enable Fortran 2003 interface')

    # Examples
    variant('examples',         default=True,
            description='Enable examples')
    variant('examples-install', default=True,
            description='Install examples')

    # Generic (std-c) math libraries (UNIX only)
    variant('generic-math', default=True,
            description='Use generic (std-c) math libraries on unix systems')

    # Monitoring
    variant('monitoring', default=False,
            description='Build with simulation monitoring capabilities')

    # ==========================================================================
    # Conflicts
    # ==========================================================================

    conflicts('+hypre',         when='@:2.6.2')
    conflicts('+petsc',         when='@:2.6.2')
    conflicts('+cuda',          when='@:2.7.0')
    conflicts('+raja',          when='@:2.7.0')
    conflicts('~int64',         when='@:2.7.0')
    conflicts('+superlu-dist',  when='@:4.1.0')
    conflicts('+f2003',         when='@:4.1.0')
    conflicts('+trilinos',      when='@:4.1.0')
    conflicts('+monitoring',    when='@:5.5.0')
    conflicts('+rocm',          when='@:5.6.0')

    # External libraries incompatible with 64-bit indices
    conflicts('+lapack', when='@3.0.0: +int64')
    conflicts('+hypre',  when='+hypre@:2.6.1a +int64')

    # External libraries incompatible with single precision
    conflicts('+klu',          when='precision=single')
    conflicts('+hypre',        when='+hypre@:2.12.0 precision=single')
    conflicts('+superlu-dist', when='precision=single')

    # External libraries incompatible with extended (quad) precision
    conflicts('+lapack',       when='precision=extended')
    conflicts('+superlu-mt',   when='precision=extended')
    conflicts('+superlu-dist', when='precision=extended')
    conflicts('+klu',          when='precision=extended')
    conflicts('+hypre',        when='+hypre@:2.12.0 precision=extended')

    # SuperLU_MT interface requires lapack for external blas (before v3.0.0)
    conflicts('+superlu-mt', when='@:2.7.0 ~lapack')

    # ==========================================================================
    # Dependencies
    # ==========================================================================

    # Build dependencies
    depends_on('cmake@3.12:', type='build')

    # MPI related dependencies
    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+hypre')
    depends_on('mpi', when='+petsc')
    depends_on('mpi', when='+superlu-dist')

    # Other parallelism dependencies
    depends_on('raja', when='+raja')

    # External libraries
    depends_on('lapack',              when='+lapack')
    depends_on('suite-sparse',        when='+klu')
    depends_on('petsc+mpi',           when='+petsc')
    depends_on('hypre+mpi',           when='+hypre')
    depends_on('superlu-dist@6.1.1:', when='@:5.4.0 +superlu-dist')
    depends_on('superlu-dist@6.3.0:', when='@5.5.0: +superlu-dist')
    depends_on('trilinos+tpetra',     when='+trilinos')

    # Require that external libraries built with the same precision
    depends_on('petsc~double~complex', when='+petsc precision=single')
    depends_on('petsc+double~complex', when='+petsc precision=double')

    # Require that external libraries built with the same index type
    depends_on('hypre~int64', when='+hypre ~int64')
    depends_on('hypre+int64', when='+hypre +int64')
    depends_on('petsc~int64', when='+petsc ~int64')
    depends_on('petsc+int64', when='+petsc +int64')
    depends_on('superlu-dist+int64', when='+superlu-dist +int64')

    # Require that SuperLU_MT built with external blas
    depends_on('superlu-mt+blas', when='+superlu-mt')

    # ==========================================================================
    # Patches
    # ==========================================================================

    # remove OpenMP header file and function from hypre vector test code
    patch('test_nvector_parhyp.patch', when='@2.7.0:3.0.0')
    patch('FindPackageMultipass.cmake.patch', when='@5.0.0')
    patch('5.5.0-xsdk-patches.patch', when='@5.5.0')
    patch('0001-add-missing-README-to-examples-cvode-hip.patch', when='@5.6.0:5.7.0')

    # ==========================================================================
    # SUNDIALS Settings
    # ==========================================================================

    def cmake_args(self):
        spec = self.spec

        def on_off(varstr):
            return 'ON' if varstr in self.spec else 'OFF'

        fortran_flag = self.compiler.f77_pic_flag
        if (spec.satisfies('%apple-clang')) and ('+fcmix' in spec):
            f77 = Executable(self.compiler.f77)
            libgfortran = LibraryList(f77('--print-file-name',
                                          'libgfortran.a', output=str))
            fortran_flag += ' ' + libgfortran.ld_flags

        # List of CMake arguments
        # Note: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE are set automatically
        args = []

        # SUNDIALS solvers
        for pkg in self.sun_solvers:
            args.extend(['-DBUILD_%s=%s' % (pkg, on_off('+' + pkg))])

        # precision
        args.extend([
            '-DSUNDIALS_PRECISION=%s' % spec.variants['precision'].value
        ])

        # index type (v3.0.0 or later)
        if spec.satisfies('@3.0.0:'):
            if '+int64' in spec:
                args.extend(['-DSUNDIALS_INDEX_SIZE=64'])
                args.extend(['-DSUNDIALS_INDEX_TYPE=int64_t'])
            else:
                args.extend(['-DSUNDIALS_INDEX_SIZE=32'])
                args.extend(['-DSUNDIALS_INDEX_TYPE=int32_t'])

        # Fortran interface
        args.extend(['-DF77_INTERFACE_ENABLE=%s' % on_off('+fcmix')])
        args.extend(['-DF2003_INTERFACE_ENABLE=%s' % on_off('+f2003')])

        # library type
        args.extend([
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared'),
            '-DBUILD_STATIC_LIBS=%s' % on_off('+static')
        ])

        # generic (std-c) math libraries
        args.extend([
            '-DUSE_GENERIC_MATH=%s' % on_off('+generic-math')
        ])

        # Monitoring
        args.extend([
            '-DSUNDIALS_BUILD_WITH_MONITORING=%s' % on_off('+monitoring')
        ])

        # parallelism
        args.extend([
            '-DMPI_ENABLE=%s'     % on_off('+mpi'),
            '-DOPENMP_ENABLE=%s'  % on_off('+openmp'),
            '-DPTHREAD_ENABLE=%s' % on_off('+pthread')
        ])

        if '+cuda' in spec:
            args.append('-DCUDA_ENABLE=ON')
            archs = spec.variants['cuda_arch'].value
            if archs != 'none':
                arch_str = ",".join(archs)
            args.append('CMAKE_CUDA_ARCHITECTURES=%s' % arch_str)
        else:
            args.append('-DCUDA_ENABLE=OFF')

        if '+rocm' in spec:
            args.extend([
                '-DCMAKE_CXX_COMPILER=%s' % spec['hip'].hipcc,
                '-DENABLE_HIP=ON',
                '-DHIP_PATH=%s' % spec['hip'].prefix,
                '-DHIP_CLANG_INCLUDE_PATH=%s/include' % spec['llvm-amdgpu'].prefix,
                '-DROCM_PATH=%s' % spec['llvm-amdgpu'].prefix
            ])
            archs = spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
            args.append('-DAMDGPU_TARGETS=%s' % arch_str)
        else:
            args.append('-DENABLE_HIP=OFF')

        # MPI support
        if '+mpi' in spec:
            args.extend([
                '-DMPI_MPICC=%s' % spec['mpi'].mpicc,
                '-DMPI_MPICXX=%s' % spec['mpi'].mpicxx,
                '-DMPI_MPIF77=%s' % spec['mpi'].mpif77,
                '-DMPI_MPIF90=%s' % spec['mpi'].mpifc
            ])

        # Building with Hypre
        if '+hypre' in spec:
            args.extend([
                '-DHYPRE_ENABLE=ON',
                '-DHYPRE_INCLUDE_DIR=%s' % spec['hypre'].prefix.include,
                '-DHYPRE_LIBRARY_DIR=%s' % spec['hypre'].prefix.lib
            ])
        else:
            args.extend([
                '-DHYPRE_ENABLE=OFF'
            ])

        # Building with KLU
        if '+klu' in spec:
            args.extend([
                '-DKLU_ENABLE=ON',
                '-DKLU_INCLUDE_DIR=%s' % spec['suite-sparse'].prefix.include,
                '-DKLU_LIBRARY_DIR=%s' % spec['suite-sparse'].prefix.lib
            ])
        else:
            args.extend([
                '-DKLU_ENABLE=OFF'
            ])

        # Building with LAPACK
        if '+lapack' in spec:
            args.extend([
                '-DLAPACK_ENABLE=ON',
                '-DLAPACK_LIBRARIES=%s'
                % (spec['lapack'].libs + spec['blas'].libs).joined(';')
            ])
        else:
            args.extend([
                '-DLAPACK_ENABLE=OFF'
            ])

        # Building with PETSc
        if '+petsc' in spec:
            args.extend([
                '-DPETSC_ENABLE=ON',
                # PETSC_DIR was added in 5.0.0
                '-DPETSC_DIR=%s'         % spec['petsc'].prefix,
                # The following options were removed 5.0.0, but we keep
                # them here for versions < 5.0.0.
                '-DPETSC_INCLUDE_DIR=%s' % spec['petsc'].prefix.include,
                '-DPETSC_LIBRARY_DIR=%s' % spec['petsc'].prefix.lib
            ])
        else:
            args.extend([
                '-DPETSC_ENABLE=OFF'
            ])

        # Building with RAJA
        if '+raja' in spec:
            args.extend([
                '-DRAJA_ENABLE=ON',
                '-DRAJA_DIR=%s' % spec['raja'].prefix.share.raja.cmake
            ])
        else:
            args.extend([
                '-DRAJA_ENABLE=OFF'
            ])

        # Building with SuperLU_MT
        if '+superlu-mt' in spec:
            if spec.satisfies('@3.0.0:'):
                args.extend([
                    '-DBLAS_ENABLE=ON',
                    '-DBLAS_LIBRARIES=%s' % spec['blas'].libs
                ])
            args.extend([
                '-DSUPERLUMT_ENABLE=ON',
                '-DSUPERLUMT_INCLUDE_DIR=%s'
                % spec['superlu-mt'].prefix.include,
                '-DSUPERLUMT_LIBRARY_DIR=%s'
                % spec['superlu-mt'].prefix.lib
            ])
            if spec.satisfies('^superlu-mt+openmp'):
                args.append('-DSUPERLUMT_THREAD_TYPE=OpenMP')
            else:
                args.append('-DSUPERLUMT_THREAD_TYPE=Pthread')
        else:
            args.extend([
                '-DSUPERLUMT_ENABLE=OFF'
            ])

        # Building with SuperLU_DIST
        if '+superlu-dist' in spec:
            args.extend([
                '-DOPENMP_ENABLE=%s'
                % on_off('^superlu-dist+openmp'),
                '-DSUPERLUDIST_ENABLE=ON',
                '-DSUPERLUDIST_INCLUDE_DIR=%s'
                % spec['superlu-dist'].prefix.include,
                '-DSUPERLUDIST_LIBRARY_DIR=%s'
                % spec['superlu-dist'].prefix.lib,
                '-DSUPERLUDIST_LIBRARIES=%s'
                % spec['blas'].libs.joined(';'),
                '-DSUPERLUDIST_OpenMP=%s'
                % on_off('^superlu-dist+openmp')
            ])
        else:
            args.extend([
                '-DSUPERLUDIST_ENABLE=OFF'
            ])

        # Building with Trilinos
        if '+trilinos' in spec:
            args.extend([
                '-DTrilinos_ENABLE=ON',
                '-DTrilinos_DIR=%s'
                % spec['trilinos'].prefix
            ])
        else:
            args.extend([
                '-DTrilinos_ENABLE=OFF'
            ])

        # Examples
        if spec.satisfies('@3.0.0:'):
            args.extend([
                '-DEXAMPLES_ENABLE_C=%s'      % on_off('+examples'),
                '-DEXAMPLES_ENABLE_CXX=%s'    % on_off('+examples'),
                '-DEXAMPLES_ENABLE_CUDA=%s'   % on_off('+examples+cuda'),
                '-DEXAMPLES_ENABLE_F77=%s'    % on_off('+examples+fcmix'),
                '-DEXAMPLES_ENABLE_F90=%s'    % on_off('+examples+fcmix'),
                '-DEXAMPLES_ENABLE_F2003=%s'  % on_off('+examples+f2003'),
            ])
        else:
            args.extend([
                '-DEXAMPLES_ENABLE=%s' % on_off('+examples'),
                '-DCXX_ENABLE=%s'      % on_off('+examples'),
                '-DF90_ENABLE=%s'      % on_off('+examples+fcmix')
            ])

        args.extend([
            '-DEXAMPLES_INSTALL=%s' % on_off('+examples-install')
        ])

        return args

    # ==========================================================================
    # Post Install Actions
    # ==========================================================================

    @run_after('install')
    def post_install(self):
        """Run after install to fix install name of dynamic libraries
        on Darwin to have full path and install the LICENSE file."""
        spec = self.spec
        prefix = self.spec.prefix

        if (sys.platform == 'darwin'):
            fix_darwin_install_name(prefix.lib)

        if spec.satisfies('@:3.0.0'):
            install('LICENSE', prefix)

    @run_after('install')
    def filter_compilers(self):
        """Run after install to tell the example program Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC, CPP, and F77 set to
        Spack's generic cc and f77. We want them to be bound to
        whatever compiler they were built with."""

        spec = self.spec

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
        dirname = os.path.join(self.prefix, 'examples')

        cc_files = [
            'arkode/C_openmp/Makefile',
            'arkode/C_parallel/Makefile',
            'arkode/C_parhyp/Makefile',
            'arkode/C_petsc/Makefile',
            'arkode/C_serial/Makefile',
            'cvode/C_openmp/Makefile',
            'cvode/parallel/Makefile',
            'cvode/parhyp/Makefile',
            'cvode/petsc/Makefile',
            'cvode/serial/Makefile',
            'cvodes/C_openmp/Makefile',
            'cvodes/parallel/Makefile',
            'cvodes/serial/Makefile',
            'ida/C_openmp/Makefile',
            'ida/parallel/Makefile',
            'ida/petsc/Makefile',
            'ida/serial/Makefile',
            'idas/C_openmp/Makefile',
            'idas/parallel/Makefile',
            'idas/serial/Makefile',
            'kinsol/C_openmp/Makefile',
            'kinsol/parallel/Makefile',
            'kinsol/serial/Makefile',
            'nvector/C_openmp/Makefile',
            'nvector/parallel/Makefile',
            'nvector/parhyp/Makefile',
            'nvector/petsc/Makefile',
            'nvector/pthreads/Makefile',
            'nvector/serial/Makefile',
            'sunlinsol/band/Makefile',
            'sunlinsol/dense/Makefile',
            'sunlinsol/klu/Makefile',
            'sunlinsol/lapackband/Makefile',
            'sunlinsol/lapackdense/Makefile',
            'sunlinsol/pcg/parallel/Makefile',
            'sunlinsol/pcg/serial/Makefile',
            'sunlinsol/spbcgs/parallel/Makefile',
            'sunlinsol/spbcgs/serial/Makefile',
            'sunlinsol/spfgmr/parallel/Makefile',
            'sunlinsol/spfgmr/serial/Makefile',
            'sunlinsol/spgmr/parallel/Makefile',
            'sunlinsol/spgmr/serial/Makefile',
            'sunlinsol/sptfqmr/parallel/Makefile',
            'sunlinsol/sptfqmr/serial/Makefile',
            'sunlinsol/superlumt/Makefile',
            'sunlinsol/superludist/Makefile',
            'sunmatrix/band/Makefile',
            'sunmatrix/dense/Makefile',
            'sunmatrix/sparse/Makefile'
        ]

        cxx_files = [
            'arkode/CXX_parallel/Makefile',
            'arkode/CXX_serial/Makefile'
            'cvode/cuda/Makefile',
            'cvode/raja/Makefile',
            'nvector/cuda/Makefile',
            'nvector/raja/Makefile'
        ]

        f77_files = [
            'arkode/F77_parallel/Makefile',
            'arkode/F77_serial/Makefile',
            'cvode/fcmix_parallel/Makefile',
            'cvode/fcmix_serial/Makefile',
            'ida/fcmix_openmp/Makefile',
            'ida/fcmix_parallel/Makefile',
            'ida/fcmix_pthreads/Makefile',
            'ida/fcmix_serial/Makefile',
            'kinsol/fcmix_parallel/Makefile',
            'kinsol/fcmix_serial/Makefile'
        ]

        f90_files = [
            'arkode/F90_parallel/Makefile',
            'arkode/F90_serial/Makefile'
        ]

        f2003_files = [
            'arkode/F2003_serial/Makefile',
            'cvode/F2003_serial/Makefile',
            'cvodes/F2003_serial/Makefike',
            'ida/F2003_serial/Makefile',
            'idas/F2003_serial/Makefile',
            'kinsol/F2003_serial/Makefile'
        ]

        for filename in cc_files:
            filter_file(os.environ['CC'], self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cc_files:
            filter_file(r'^CPP\s*=.*', self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(os.environ['CXX'], self.compiler.cxx,
                        os.path.join(dirname, filename), **kwargs)

        for filename in cxx_files:
            filter_file(r'^CPP\s*=.*', self.compiler.cc,
                        os.path.join(dirname, filename), **kwargs)

        if ('+fcmix' in spec) and ('+examples' in spec):
            for filename in f77_files:
                filter_file(os.environ['F77'], self.compiler.f77,
                            os.path.join(dirname, filename), **kwargs)

        if ('+fcmix' in spec) and ('+examples' in spec):
            for filename in f90_files:
                filter_file(os.environ['FC'], self.compiler.fc,
                            os.path.join(dirname, filename), **kwargs)

        if ('+f2003' in spec) and ('+examples' in spec):
            for filename in f2003_files:
                filter_file(os.environ['FC'], self.compiler.fc,
                            os.path.join(dirname, filename), **kwargs)

    @property
    def headers(self):
        """Export the headers and defines of SUNDIALS.
           Sample usage: spec['sundials'].headers.cpp_flags
        """
        # SUNDIALS headers are inside subdirectories, so we use a fake header
        # in the include directory.
        hdr = find(self.prefix.include.nvector, 'nvector_serial.h',
                   recursive=False)
        return HeaderList(join_path(self.spec.prefix.include, 'fake.h')) \
            if hdr else None

    @property
    def libs(self):
        """Export the libraries of SUNDIALS.
           Sample usage: spec['sundials'].libs.ld_flags
                         spec['sundials:arkode,cvode'].libs.ld_flags
        """
        query_parameters = self.spec.last_query.extra_parameters
        if not query_parameters:
            sun_libs = 'libsundials_*[!0-9]'
            # Q: should the result be ordered by dependency?
        else:
            sun_libs = ['libsundials_' + p for p in query_parameters]
        is_shared = '+shared' in self.spec

        libs = find_libraries(sun_libs, root=self.prefix, shared=is_shared,
                              recursive=True)

        return libs or None  # Raise an error if no libs are found

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        """Perform make test_install.
        """
        with working_dir(self.build_directory):
            make("test_install")

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to a
        relative install test subdirectory for use during `spack test run`."""
        # Now copy the relative files
        self.cache_extra_test_sources(self.build_relpath)

        # Ensure the path exists since relying on a relative path at the
        # same level as the normal stage source path.
        mkdirp(self.install_test_root)

    @property
    def build_relpath(self):
        """Relative path to the cmake build subdirectory."""
        return join_path('..', self.build_dirname)

    @property
    def _extra_tests_path(self):
        return join_path(self.install_test_root, self.build_relpath)

    def test(self):
        """Run the smoke tests."""
        if '+examples' not in self.spec:
            print('Smoke tests were skipped: install with examples enabled')
        return

        self.run_test('examples/nvector/serial/test_nvector_serial',
                      options=['10', '0'],
                      work_dir=self._extra_tests_path)
        if '+cuda' in self.spec:
            self.run_test('examples/cvode/cuda/cvAdvDiff_ky_cuda',
                          work_dir=self._extra_tests_path)
            self.run_test('examples/nvector/cuda/test_nvector_cuda',
                          options=['10', '0', '0'],
                          work_dir=self._extra_tests_path)
        if '+rocm' in self.spec:
            self.run_test('examples/cvode/hip/cvAdvDiff_kry_hip',
                          work_dir=self._extra_tests_path)
            self.run_test('examples/nvector/hip/test_nvector_hip',
                          options=['10', '0', '0'],
                          work_dir=self._extra_tests_path)
        return
