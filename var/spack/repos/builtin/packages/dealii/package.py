# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dealii(CMakePackage, CudaPackage):
    """C++ software library providing well-documented tools to build finite
    element codes for a broad variety of PDEs."""

    homepage = "https://www.dealii.org"
    url      = "https://github.com/dealii/dealii/releases/download/v8.4.1/dealii-8.4.1.tar.gz"
    git      = "https://github.com/dealii/dealii.git"

    maintainers = ['davydden', 'jppelteret']

    # Don't add RPATHs to this package for the full build DAG.
    # only add for immediate deps.
    transitive_rpaths = False

    version('develop', branch='master')
    version('9.1.1', sha256='fc5b483f7fe58dfeb52d05054011280f115498e337af3e085bf272fd1fd81276')
    version('9.1.0', sha256='5b070112403f8afbb72345c1bb24d2a38d11ce58891217e353aab97957a04600')
    version('9.0.1', sha256='df2f0d666f2224be07e3741c0e8e02132fd67ea4579cd16a2429f7416146ee64')
    version('9.0.0', sha256='c918dc5c1a31d62f6eea7b524dcc81c6d00b3c378d4ed6965a708ab548944f08')
    version('8.5.1', sha256='d33e812c21a51f7e5e3d3e6af86aec343155650b611d61c1891fbc3cabce09ae')
    version('8.5.0', sha256='e6913ff6f184d16bc2598c1ba31f879535b72b6dff043e15aef048043ff1d779')
    version('8.4.2', sha256='ec7c00fadc9d298d1a0d16c08fb26818868410a9622c59ba624096872f3058e4')
    version('8.4.1', sha256='00a0e92d069cdafd216816f1aff460f7dbd48744b0d9e0da193287ebf7d6b3ad')
    version('8.4.0', sha256='36a20e097a03f17b557e11aad1400af8c6252d25f7feca40b611d5fc16d71990')
    version('8.3.0', sha256='4ddf72632eb501e1c814e299f32fc04fd680d6fda9daff58be4209e400e41779')
    version('8.2.1', sha256='d75674e45fe63cd9fa294460fe45228904d51a68f744dbb99cd7b60720f3b2a0')
    version('8.1.0', sha256='d666bbda2a17b41b80221d7029468246f2658051b8c00d9c5907cd6434c4df99')

    variant('mpi',      default=True,  description='Compile with MPI')
    variant('mkl64',    default=False,  description='Build with 64 bit MKL interface')
    variant('assimp',   default=True,
            description='Compile with Assimp')
    variant('arpack',   default=True,
            description='Compile with Arpack and PArpack (only with MPI)')
    variant('adol-c',   default=True,
            description='Compile with Adol-c')
    variant('doc',      default=False,
            description='Compile with documentation')
    variant('ginkgo',   default=True, description='Compile with Ginkgo')
    variant('gmsh',     default=True,  description='Compile with GMSH')
    variant('gsl',      default=True,  description='Compile with GSL')
    variant('hdf5',     default=True,
            description='Compile with HDF5 (only with MPI)')
    variant('metis',    default=True,  description='Compile with Metis')
    variant('muparser', default=True,  description='Compile with muParser')
    variant('nanoflann', default=True, description='Compile with Nanoflann')
    variant('netcdf',   default=True,
            description='Compile with Netcdf (only with MPI)')
    variant('oce',      default=True,  description='Compile with OCE')
    variant('p4est',    default=True,
            description='Compile with P4est (only with MPI)')
    variant('petsc',    default=True,
            description='Compile with Petsc (only with MPI)')
    variant('scalapack', default=True,
            description='Compile with ScaLAPACK (only with MPI)')
    variant('sundials', default=True,
            description='Compile with Sundials')
    variant('slepc',    default=True,
            description='Compile with Slepc (only with Petsc and MPI)')
    variant('symengine', default=True,
            description='Compile with SymEngine')
    variant('threads',  default=True,
            description='Compile with multi-threading via TBB')
    variant('trilinos', default=True,
            description='Compile with Trilinos (only with MPI)')
    variant('python',   default=False,
            description='Compile with Python bindings')
    variant('int64',    default=False,
            description='Compile with 64 bit indices support')
    variant('optflags', default=False,
            description='Compile using additional optimization flags')
    variant('build_type', default='DebugRelease',
            description='The build type to build',
            values=('Debug', 'Release', 'DebugRelease'))

    # required dependencies, light version
    depends_on('blas')
    # Boost 1.58 is blacklisted, require at least 1.59, see
    # https://github.com/dealii/dealii/issues/1591
    # There are issues with 1.65.1 and 1.65.0:
    # https://github.com/dealii/dealii/issues/5262
    # we take the patch from https://github.com/boostorg/serialization/pull/79
    # more precisely its variation https://github.com/dealii/dealii/pull/5572#issuecomment-349742019
    # 1.68.0 has issues with serialization https://github.com/dealii/dealii/issues/7074
    # adopt https://github.com/boostorg/serialization/pull/105 as a fix
    depends_on('boost@1.59.0:1.63,1.65.1,1.67.0:+thread+system+serialization+iostreams',
               patches=[patch('boost_1.65.1_singleton.patch',
                              level=1,
                              when='@1.65.1'),
                        patch('boost_1.68.0.patch',
                              level=1,
                              when='@1.68.0'),
                        ],
               when='~python')
    depends_on('boost@1.59.0:1.63,1.65.1,1.67.0:+thread+system+serialization+iostreams+python',
               patches=[patch('boost_1.65.1_singleton.patch',
                              level=1,
                              when='@1.65.1'),
                        patch('boost_1.68.0.patch',
                              level=1,
                              when='@1.68.0'),
                        ],
               when='+python')
    # bzip2 is not needed since 9.0
    depends_on('bzip2', when='@:8.99')
    depends_on('lapack')
    depends_on('suite-sparse')
    depends_on('zlib')

    # optional dependencies
    depends_on('mpi',              when='+mpi')
    depends_on('adol-c@2.6.4:',    when='@9.0:+adol-c')
    depends_on('arpack-ng+mpi',    when='+arpack+mpi')
    depends_on('assimp',           when='@9.0:+assimp')
    depends_on('doxygen+graphviz', when='+doc')
    depends_on('graphviz',         when='+doc')
    depends_on('ginkgo',           when='@9.1:+ginkgo')
    depends_on('gmsh+tetgen+netgen+oce', when='@9.0:+gmsh', type=('build', 'run'))
    depends_on('gsl',              when='@8.5.0:+gsl')
    # FIXME: next line fixes concretization with petsc
    depends_on('hdf5+mpi+hl+fortran', when='+hdf5+mpi+petsc')
    depends_on('hdf5+mpi+hl', when='+hdf5+mpi~petsc')
    depends_on('cuda@8:',          when='+cuda')
    depends_on('cmake@3.9:',       when='+cuda', type='build')
    # older version of deal.II do not build with Cmake 3.10, see
    # https://github.com/dealii/dealii/issues/5510
    depends_on('cmake@:3.9.99',    when='@:8.99', type='build')
    # FIXME: concretizer bug. The two lines mimic what comes from PETSc
    # but we should not need it
    depends_on('metis@5:+int64',   when='+metis+int64')
    depends_on('metis@5:~int64',   when='+metis~int64')
    depends_on('muparser', when='+muparser')
    depends_on('nanoflann',        when='@9.0:+nanoflann')
    depends_on('netcdf-c+mpi',     when='+netcdf+mpi')
    depends_on('netcdf-cxx',       when='+netcdf+mpi')
    depends_on('oce',              when='+oce')
    depends_on('p4est',            when='+p4est+mpi')
    depends_on('petsc+mpi~int64',  when='+petsc+mpi~int64')
    depends_on('petsc+mpi+int64',  when='+petsc+mpi+int64')
    depends_on('petsc@:3.6.4',     when='@:8.4.1+petsc+mpi')
    depends_on('python',           when='@8.5.0:+python')
    depends_on('scalapack',        when='@9.0:+scalapack')
    depends_on('slepc',            when='+slepc+petsc+mpi')
    depends_on('slepc@:3.6.3',     when='@:8.4.1+slepc+petsc+mpi')
    depends_on('slepc~arpack',     when='+slepc+petsc+mpi+int64')
    depends_on('sundials@:3~pthread', when='@9.0:+sundials')
    depends_on('trilinos gotype=int', when='+trilinos')
    # Both Trilinos and SymEngine bundle the Teuchos RCP library.
    # This leads to conflicts between macros defined in the included
    # headers when they are not compiled in the same mode.
    # See https://github.com/symengine/symengine/issues/1516
    # FIXME: uncomment when the following is fixed
    # https://github.com/spack/spack/issues/11160
    # depends_on("symengine@0.4: build_type=Release", when="@9.1:+symengine+trilinos^trilinos~debug")  # NOQA: ignore=E501
    # depends_on("symengine@0.4: build_type=Debug", when="@9.1:+symengine+trilinos^trilinos+debug")  # NOQA: ignore=E501
    depends_on('symengine@0.4:', when='@9.1:+symengine')
    depends_on('tbb', when='+threads')
    # do not require +rol to make concretization of xsdk possible
    depends_on('trilinos+amesos+aztec+epetra+ifpack+ml+muelu+sacado+teuchos',       when='+trilinos+mpi~int64~cuda')
    depends_on('trilinos+amesos+aztec+epetra+ifpack+ml+muelu+sacado+teuchos~hypre', when='+trilinos+mpi+int64~cuda')
    # FIXME: temporary disable Tpetra when using CUDA due to
    # namespace "Kokkos::Impl" has no member "cuda_abort"
    depends_on('trilinos@master+amesos+aztec+epetra+ifpack+ml+muelu+rol+sacado+teuchos~amesos2~ifpack2~intrepid2~kokkos~tpetra~zoltan2',       when='+trilinos+mpi~int64+cuda')
    depends_on('trilinos@master+amesos+aztec+epetra+ifpack+ml+muelu+rol+sacado+teuchos~hypre~amesos2~ifpack2~intrepid2~kokkos~tpetra~zoltan2', when='+trilinos+mpi+int64+cuda')

    # Explicitly provide a destructor in BlockVector,
    # otherwise deal.II may fail to build with Intel compilers.
    patch('https://github.com/dealii/dealii/commit/a89d90f9993ee9ad39e492af466b3595c06c3e25.patch',
          sha256='4282b32e96f2f5d376eb34f3fddcc4615fcd99b40004cca784eb874288d1b31c',
          when='@9.0.1')

    # https://github.com/dealii/dealii/pull/7935
    patch('https://github.com/dealii/dealii/commit/f8de8c5c28c715717bf8a086e94f071e0fe9deab.patch',
          sha256='61f217744b70f352965be265d2f06e8c1276685e2944ca0a88b7297dd55755da',
          when='@9.0.1 ^boost@1.70.0:')

    # Fix TBB version check
    # https://github.com/dealii/dealii/pull/9208
    patch('https://github.com/dealii/dealii/commit/80b13fe5a2eaefc77fa8c9266566fa8a2de91edf.patch',
          sha256='6f876dc8eadafe2c4ec2a6673864fb451c6627ca80511b6e16f3c401946fdf33',
          when='@9.0.0:9.1.1')

    # check that the combination of variants makes sense
    # 64-bit BLAS:
    conflicts('^openblas+ilp64', when='@:8.5.1', 
              msg='64bit OpenBLAS is only supported from 9.0.0')
    conflicts('+mkl64', when='@:8.5.1',
              msg='64bit MKL is only supported from 9.0.0')


    # interfaces added in 9.0.0:
    for p in ['assimp', 'gmsh', 'nanoflann', 'scalapack', 'sundials',
              'adol-c']:
        conflicts('+{0}'.format(p), when='@:8.5.1',
                  msg='The interface to {0} is supported from version 9.0.0 '
                      'onwards. Please explicitly disable this variant '
                      'via ~{0}'.format(p))

    # interfaces added in 9.1.0:
    for p in ['ginkgo', 'symengine']:
        conflicts('+{0}'.format(p), when='@:9.0',
                  msg='The interface to {0} is supported from version 9.1.0 '
                      'onwards. Please explicitly disable this variant '
                      'via ~{0}'.format(p))

    conflicts('+slepc', when='~petsc',
              msg='It is not possible to enable slepc interfaces '
                  'without petsc.')

    conflicts('+adol-c', when='^trilinos+chaco',
              msg='symbol clash between the ADOL-C library and '
                  'Trilinos SEACAS Chaco.')

    # interfaces added in 8.5.0:
    for p in ['gsl', 'python']:
        conflicts('+{0}'.format(p), when='@:8.4.2',
                  msg='The interface to {0} is supported from version 8.5.0 '
                      'onwards. Please explicitly disable this variant '
                      'via ~{0}'.format(p))

    # MPI requirements:
    for p in ['arpack', 'hdf5', 'netcdf', 'p4est', 'petsc', 'scalapack',
              'slepc', 'trilinos']:
        conflicts('+{0}'.format(p), when='~mpi',
                  msg='To enable {0} it is necessary to build deal.II with '
                      'MPI support enabled.'.format(p))

    def cmake_args(self):
        spec = self.spec
        options = []
        # release flags
        cxx_flags_release = []
        # debug and release flags
        cxx_flags = []

        lapack_blas_libs = spec['lapack'].libs + spec['blas'].libs
        lapack_blas_headers = spec['lapack'].headers + spec['blas'].headers
        options.extend([
            '-DDEAL_II_COMPONENT_EXAMPLES=ON',
            '-DBOOST_DIR=%s' % spec['boost'].prefix,
            # CMake's FindBlas/Lapack may pickup system's blas/lapack instead
            # of Spack's. Be more specific to avoid this.
            # Note that both lapack and blas are provided in -DLAPACK_XYZ.
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS=%s' % ';'.join(
                lapack_blas_headers.directories),
            '-DLAPACK_LIBRARIES=%s' % lapack_blas_libs.joined(';'),
            '-DUMFPACK_DIR=%s' % spec['suite-sparse'].prefix,
            '-DZLIB_DIR=%s' % spec['zlib'].prefix,
            '-DDEAL_II_ALLOW_BUNDLED=OFF'
        ])

        if '+threads' in spec:
            options.append('-DDEAL_II_WITH_THREADS:BOOL=ON')
        else:
            options.extend(['-DDEAL_II_WITH_THREADS:BOOL=OFF'])

        if '^tbb' in spec and '+threads' in spec:
            # deal.II/cmake will have hard time picking up TBB from Intel.
            tbb_ver = '.'.join(('%s' % spec['tbb'].version).split('.')[1:])
            options.extend([
                '-DTBB_FOUND=true',
                '-DTBB_VERSION=%s' % tbb_ver,
                '-DTBB_INCLUDE_DIRS=%s' % ';'.join(
                    spec['tbb'].headers.directories),
                '-DTBB_LIBRARIES=%s' % spec['tbb'].libs.joined(';')
            ])
        else:
            options.append('-DTBB_DIR=%s' % spec['tbb'].prefix)

        if '^openblas+ilp64' in spec or ('^mkl' in spec and '+mkl64' in spec):
            options.append('-DLAPACK_WITH_64BIT_BLAS_INDICES=ON')

        if spec.satisfies('@:8.99'):
            options.extend([
                # Cmake may still pick up system's bzip2, fix this:
                '-DBZIP2_FOUND=true',
                '-DBZIP2_INCLUDE_DIRS=%s' % spec['bzip2'].prefix.include,
                '-DBZIP2_LIBRARIES=%s' % spec['bzip2'].libs.joined(';')
            ])

        # Set recommended flags for maximum (matrix-free) performance, see
        # https://groups.google.com/forum/?fromgroups#!topic/dealii/3Yjy8CBIrgU
        if spec.satisfies('%gcc'):
            cxx_flags_release.extend(['-O3'])
        elif spec.satisfies('%intel'):
            cxx_flags_release.extend(['-O3'])
        elif spec.satisfies('%clang'):
            cxx_flags_release.extend(['-O3', '-ffp-contract=fast'])

        # Python bindings
        if spec.satisfies('@8.5.0:'):
            options.extend([
                '-DDEAL_II_COMPONENT_PYTHON_BINDINGS=%s' %
                ('ON' if '+python' in spec else 'OFF')
            ])
            if '+python' in spec:
                python_exe = spec['python'].command.path
                python_library = spec['python'].libs[0]
                python_include = spec['python'].headers.directories[0]
                options.extend([
                    '-DPYTHON_EXECUTABLE=%s' % python_exe,
                    '-DPYTHON_INCLUDE_DIR=%s' % python_include,
                    '-DPYTHON_LIBRARY=%s' % python_library
                ])

        # Set directory structure:
        if spec.satisfies('@:8.2.1'):
            options.extend(['-DDEAL_II_COMPONENT_COMPAT_FILES=OFF'])
        else:
            options.extend([
                '-DDEAL_II_EXAMPLES_RELDIR=share/deal.II/examples',
                '-DDEAL_II_DOCREADME_RELDIR=share/deal.II/',
                '-DDEAL_II_DOCHTML_RELDIR=share/deal.II/doc'
            ])

        # CUDA
        if '+cuda' in spec:
            options.append(
                '-DDEAL_II_WITH_CUDA=ON'
            )
            if not spec.satisfies('^cuda@9:'):
                options.append('-DDEAL_II_WITH_CXX14=OFF')
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch != 'none':
                if len(cuda_arch) > 1:
                    raise InstallError(
                        'deal.II only supports compilation for a single GPU!'
                    )
                flags = '-arch=sm_{0}'.format(cuda_arch[0])
                # FIXME: there are some compiler errors in dealii
                # with: flags = ' '.join(self.cuda_flags(cuda_arch))
                # Stick with -arch=sm_xy for now.
                options.append(
                    '-DDEAL_II_CUDA_FLAGS={0}'.format(flags)
                )
        else:
            options.extend([
                '-DDEAL_II_WITH_CUDA=OFF',
            ])

        # MPI
        if '+mpi' in spec:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=ON',
                '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=OFF',
            ])

        # Optional dependencies for which library names are the same as CMake
        # variables:
        for library in (
                'gsl', 'hdf5', 'p4est', 'petsc', 'slepc', 'trilinos', 'metis',
                'sundials', 'nanoflann', 'assimp', 'gmsh', 'muparser',
                'symengine', 'ginkgo'):
            if ('+' + library) in spec:
                options.extend([
                    '-D%s_DIR=%s' % (library.upper(), spec[library].prefix),
                    '-DDEAL_II_WITH_%s:BOOL=ON' % library.upper()
                ])
            else:
                options.extend([
                    '-DDEAL_II_WITH_%s:BOOL=OFF' % library.upper()
                ])

        # adol-c
        if '+adol-c' in spec:
            options.extend([
                '-DADOLC_DIR=%s' % spec['adol-c'].prefix,
                '-DDEAL_II_WITH_ADOLC=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ADOLC=OFF'
            ])

        # doxygen
        options.extend([
            '-DDEAL_II_COMPONENT_DOCUMENTATION=%s' %
            ('ON' if '+doc' in spec else 'OFF'),
        ])

        # arpack
        if '+arpack' in spec and '+mpi' in spec:
            options.extend([
                '-DARPACK_DIR=%s' % spec['arpack-ng'].prefix,
                '-DDEAL_II_WITH_ARPACK=ON',
                '-DDEAL_II_ARPACK_WITH_PARPACK=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ARPACK=OFF'
            ])

        # since Netcdf is spread among two, need to do it by hand:
        if '+netcdf' in spec and '+mpi' in spec:
            netcdf = spec['netcdf-cxx'].libs + spec['netcdf-c'].libs
            options.extend([
                '-DNETCDF_FOUND=true',
                '-DNETCDF_LIBRARIES=%s' % netcdf.joined(';'),
                '-DNETCDF_INCLUDE_DIRS=%s;%s' % (
                    spec['netcdf-cxx'].prefix.include,
                    spec['netcdf-c'].prefix.include),
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_NETCDF=OFF'
            ])

        if '+scalapack' in spec:
            scalapack = spec['scalapack'].libs
            options.extend([
                '-DSCALAPACK_FOUND=true',
                '-DSCALAPACK_INCLUDE_DIRS=%s' % (
                    spec['scalapack'].prefix.include),
                '-DSCALAPACK_LIBRARIES=%s' % scalapack.joined(';'),
                '-DDEAL_II_WITH_SCALAPACK=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_SCALAPACK=OFF'
            ])

        # Open Cascade
        if '+oce' in spec:
            options.extend([
                '-DOPENCASCADE_DIR=%s' % spec['oce'].prefix,
                '-DDEAL_II_WITH_OPENCASCADE=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_OPENCASCADE=OFF'
            ])

        # 64 bit indices
        options.extend([
            '-DDEAL_II_WITH_64BIT_INDICES=%s' % ('+int64' in spec)
        ])

        # collect CXX flags:
        if len(cxx_flags_release) > 0 and '+optflags' in spec:
            options.extend([
                '-DCMAKE_CXX_FLAGS_RELEASE:STRING=%s' % (
                    ' '.join(cxx_flags_release)),
                '-DCMAKE_CXX_FLAGS:STRING=%s' % (
                    ' '.join(cxx_flags))
            ])

        return options

    def setup_run_environment(self, env):
        env.set('DEAL_II_DIR', self.prefix)
