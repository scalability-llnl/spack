# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dealii(CMakePackage, CudaPackage):
    """C++ software library providing well-documented tools to build finite
    element codes for a broad variety of PDEs."""

    homepage = "https://www.dealii.org"
    url      = "https://github.com/dealii/dealii/releases/download/v8.4.1/dealii-8.4.1.tar.gz"
    git      = "https://github.com/dealii/dealii.git"

    maintainers = ['davydden', 'jppelteret', 'luca-heltai']

    # Don't add RPATHs to this package for the full build DAG.
    # only add for immediate deps.
    transitive_rpaths = False

    generator = 'Ninja'

    version('master', branch='master')
    version('9.2.0', sha256='d05a82fb40f1f1e24407451814b5a6004e39366a44c81208b1ae9d65f3efa43a')
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

    # Configuration variants
    variant('build_type', default='DebugRelease',
            description='The build type to build',
            values=('Debug', 'Release', 'DebugRelease'))
    variant('cxxstd',   default='default', multi=False,
            description='Compile using the specified C++ standard',
            values=('default', '11', '14', '17'))
    variant('doc',      default=False,
            description='Compile with documentation')
    variant('examples', default=True,
            description='Compile tutorial programs')
    variant('int64',    default=False,
            description='Compile with 64 bit indices support')
    variant('mpi',      default=True,
            description='Compile with MPI')
    variant('optflags', default=False,
            description='Compile using additional optimization flags')
    variant('python',   default=False,
            description='Compile with Python bindings')

    # Package variants
    variant('assimp',   default=True,
            description='Compile with Assimp')
    variant('arpack',   default=True,
            description='Compile with Arpack and PArpack (only with MPI)')
    variant('adol-c',   default=True,
            description='Compile with ADOL-C')
    variant('ginkgo',   default=True,
            description='Compile with Ginkgo')
    variant('gmsh',     default=True,
            description='Compile with GMSH')
    variant('gsl',      default=True,
            description='Compile with GSL')
    variant('hdf5',     default=True,
            description='Compile with HDF5 (only with MPI)')
    variant('metis',    default=True,
            description='Compile with Metis')
    variant('muparser', default=True,
            description='Compile with muParser')
    variant('nanoflann', default=True,
            description='Compile with Nanoflann')
    variant('netcdf',   default=False,
            description='Compile with Netcdf (only with MPI)')
    variant('oce',      default=True,
            description='Compile with OCE')
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

    # Required dependencies: Light version
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
    # The std::auto_ptr is removed in the C++ 17 standard.
    # See https://github.com/dealii/dealii/issues/4662
    # and related topics discussed for other software libraries.
    depends_on('boost cxxstd=11', when='cxxstd=11')
    depends_on('boost cxxstd=14', when='cxxstd=14')
    depends_on('boost cxxstd=17', when='cxxstd=17')
    depends_on('bzip2',           when='@:8.99')
    depends_on('lapack')
    depends_on('ninja',           type='build')
    depends_on('suite-sparse')
    depends_on('zlib')

    # Optional dependencies: Configuration
    depends_on('cuda@8:',          when='+cuda')
    depends_on('cmake@3.9:',       when='+cuda', type='build')
    # Older version of deal.II do not build with Cmake 3.10, see
    # https://github.com/dealii/dealii/issues/5510
    depends_on('cmake@:3.9.99',    when='@:8.99', type='build')
    depends_on('mpi',              when='+mpi')
    depends_on('python',           when='@8.5.0:+python')

    # Optional dependencies: Packages
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
    depends_on('hdf5+mpi+hl',      when='+hdf5+mpi~petsc')
    # FIXME: concretizer bug. The two lines mimic what comes from PETSc
    # but we should not need it
    depends_on('metis@5:+int64',   when='+metis+int64')
    depends_on('metis@5:~int64',   when='+metis~int64')
    depends_on('muparser',         when='+muparser')
    # Nanoflann support has been removed after 9.2.0
    depends_on('nanoflann',        when='@9.0:9.2+nanoflann')
    depends_on('netcdf-c+mpi',     when='+netcdf+mpi')
    depends_on('netcdf-cxx',       when='+netcdf+mpi')
    depends_on('oce',              when='+oce')
    depends_on('p4est',            when='+p4est+mpi')
    depends_on('petsc+mpi~int64',  when='+petsc+mpi~int64')
    depends_on('petsc+mpi+int64',  when='+petsc+mpi+int64')
    depends_on('petsc@:3.6.4',     when='@:8.4.1+petsc+mpi')
    depends_on('scalapack',        when='@9.0:+scalapack')
    depends_on('slepc',            when='+slepc+petsc+mpi')
    depends_on('slepc@:3.6.3',     when='@:8.4.1+slepc+petsc+mpi')
    depends_on('slepc~arpack',     when='+slepc+petsc+mpi+int64')
    depends_on('sundials@:3~pthread', when='@9.0:+sundials')
    depends_on('trilinos gotype=int', when='+trilinos@12.18.1:')
    # Both Trilinos and SymEngine bundle the Teuchos RCP library.
    # This leads to conflicts between macros defined in the included
    # headers when they are not compiled in the same mode.
    # See https://github.com/symengine/symengine/issues/1516
    # FIXME: uncomment when the following is fixed
    # https://github.com/spack/spack/issues/11160
    # depends_on("symengine@0.4: build_type=Release", when="@9.1:+symengine+trilinos^trilinos~debug")  # NOQA: ignore=E501
    # depends_on("symengine@0.4: build_type=Debug", when="@9.1:+symengine+trilinos^trilinos+debug")  # NOQA: ignore=E501
    depends_on('symengine@0.4:', when='@9.1:+symengine')
    depends_on('symengine@0.6:', when='@9.2:+symengine')
    depends_on('tbb',            when='+threads')
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

    # Check for sufficiently modern versions
    conflicts('cxxstd=11', when='@9.3:')

    # Interfaces added in 8.5.0:
    for p in ['gsl', 'python']:
        conflicts('+{0}'.format(p), when='@:8.4.2',
                  msg='The interface to {0} is supported from version 8.5.0 '
                      'onwards. Please explicitly disable this variant '
                      'via ~{0}'.format(p))

    # Interfaces added in 9.0.0:
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

    # Interfaces removed in 9.3.0:
    conflicts('+nanoflann', when='@9.3.0:',
              msg='The interface to Nanoflann was removed from version 9.3.0. '
                  'Please explicitly disable this variant via ~nanoflann')

    # Check that the combination of variants makes sense
    # 64-bit BLAS:
    for p in ['openblas', 'intel-mkl', 'intel-parallel-studio+mkl']:
        conflicts('^{0}+ilp64'.format(p), when='@:8.5.1',
                  msg='64bit BLAS is only supported from 9.0.0')

    # MPI requirements:
    for p in ['arpack', 'hdf5', 'netcdf', 'p4est', 'petsc', 'scalapack',
              'slepc', 'trilinos']:
        conflicts('+{0}'.format(p), when='~mpi',
                  msg='To enable {0} it is necessary to build deal.II with '
                      'MPI support enabled.'.format(p))

    # Optional dependencies:
    conflicts('+adol-c', when='^netcdf',
              msg='Symbol clash between the ADOL-C library and '
                  'Netcdf.')
    conflicts('+adol-c', when='^trilinos+chaco',
              msg='Symbol clash between the ADOL-C library and '
                  'Trilinos SEACAS Chaco.')
    conflicts('+adol-c', when='^trilinos+netcdf',
              msg='Symbol clash between the ADOL-C library and '
                  'Trilinos Netcdf.')
    conflicts('+adol-c', when='^trilinos+pnetcdf',
              msg='Symbol clash between the ADOL-C library and '
                  'Trilinos parallel Netcdf.')

    conflicts('+slepc', when='~petsc',
              msg='It is not possible to enable slepc interfaces '
                  'without petsc.')

    def cmake_args(self):
        spec = self.spec
        options = []
        # Release flags
        cxx_flags_release = []
        # Debug and release flags
        cxx_flags = []

        # Set directory structure:
        if spec.satisfies('@:8.2.1'):
            options.append(
                self.define('DEAL_II_COMPONENT_COMPAT_FILES', False)
            )
        else:
            options.extend([
                self.define(
                    'DEAL_II_EXAMPLES_RELDIR', 'share/deal.II/examples'
                ),
                self.define('DEAL_II_DOCREADME_RELDIR', 'share/deal.II/'),
                self.define('DEAL_II_DOCHTML_RELDIR', 'share/deal.II/doc')
            ])

        # Required dependencies
        lapack_blas_libs = spec['lapack'].libs + spec['blas'].libs
        lapack_blas_headers = spec['lapack'].headers + spec['blas'].headers
        options.extend([
            self.define('BOOST_DIR', spec['boost'].prefix),
            # CMake's FindBlas/Lapack may pickup system's blas/lapack instead
            # of Spack's. Be more specific to avoid this.
            # Note that both lapack and blas are provided in -DLAPACK_XYZ.
            self.define('LAPACK_FOUND', True),
            self.define(
                'LAPACK_INCLUDE_DIRS',
                ';'.join(lapack_blas_headers.directories)
            ),
            self.define('LAPACK_LIBRARIES', lapack_blas_libs.joined(';')),
            self.define('UMFPACK_DIR', spec['suite-sparse'].prefix),
            self.define('ZLIB_DIR', spec['zlib'].prefix),
            self.define('DEAL_II_ALLOW_BUNDLED', False)
        ])

        if spec.satisfies('@:8.99'):
            options.extend([
                # Cmake may still pick up system's bzip2, fix this:
                self.define('BZIP2_FOUND', True),
                self.define(
                    'BZIP2_INCLUDE_DIRS', spec['bzip2'].prefix.include
                ),
                self.define('BZIP2_LIBRARIES', spec['bzip2'].libs.joined(';'))
            ])

        # Doxygen documentation
        options.append(self.define_from_variant(
            'DEAL_II_COMPONENT_DOCUMENTATION', 'doc'
        ))

        # Examples / tutorial programs
        options.append(self.define_from_variant(
            'DEAL_II_COMPONENT_EXAMPLES', 'examples'
        ))

        # Enforce the specified C++ standard
        if spec.variants['cxxstd'].value != 'default':
            cxxstd = spec.variants['cxxstd'].value
            options.append(
                self.define('DEAL_II_WITH_CXX{0}'.format(cxxstd), True)
            )

        # Performance
        # Set recommended flags for maximum (matrix-free) performance, see
        # https://groups.google.com/forum/?fromgroups#!topic/dealii/3Yjy8CBIrgU
        if spec.satisfies('%gcc'):
            cxx_flags_release.extend(['-O3'])
        elif spec.satisfies('%intel'):
            cxx_flags_release.extend(['-O3'])
        elif spec.satisfies('%clang') or spec.satisfies('%apple-clang'):
            cxx_flags_release.extend(['-O3', '-ffp-contract=fast'])

        # 64 bit indices
        options.append(self.define_from_variant(
            'DEAL_II_WITH_64BIT_INDICES', 'int64'
        ))

        if (spec.satisfies('^openblas+ilp64') or
            spec.satisfies('^intel-mkl+ilp64') or
            spec.satisfies('^intel-parallel-studio+mkl+ilp64')):
            options.append(
                self.define('LAPACK_WITH_64BIT_BLAS_INDICES', True)
            )

        # CUDA
        options.append(self.define_from_variant(
            'DEAL_II_WITH_CUDA', 'cuda'
        ))
        if '+cuda' in spec:
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
                    self.define('DEAL_II_CUDA_FLAGS', flags)
                )

        # MPI
        options.append(self.define_from_variant(
            'DEAL_II_WITH_MPI', 'mpi'
        ))
        if '+mpi' in spec:
            options.extend([
                self.define('CMAKE_C_COMPILER', spec['mpi'].mpicc),
                self.define('CMAKE_CXX_COMPILER', spec['mpi'].mpicxx),
                self.define('CMAKE_Fortran_COMPILER', spec['mpi'].mpifc),
                self.define('MPI_C_COMPILER', spec['mpi'].mpicc),
                self.define('MPI_CXX_COMPILER', spec['mpi'].mpicxx),
                self.define('MPI_Fortran_COMPILER', spec['mpi'].mpifc)
            ])
            if '+cuda' in spec:
                options.extend([
                    self.define('DEAL_II_MPI_WITH_CUDA_SUPPORT',
                                spec['mpi'].satisfies('+cuda')),
                    self.define('CUDA_HOST_COMPILER', spec['mpi'].mpicxx)
                ])

        # Python bindings
        if spec.satisfies('@8.5.0:'):
            options.append(self.define_from_variant(
                'DEAL_II_COMPONENT_PYTHON_BINDINGS', 'python'
            ))
            if '+python' in spec:
                python_exe = spec['python'].command.path
                python_library = spec['python'].libs[0]
                python_include = spec['python'].headers.directories[0]
                options.extend([
                    self.define('PYTHON_EXECUTABLE', python_exe),
                    self.define('PYTHON_INCLUDE_DIR', python_include),
                    self.define('PYTHON_LIBRARY', python_library)
                ])

        # Threading
        options.append(self.define_from_variant(
            'DEAL_II_WITH_THREADS', 'threads'
        ))
        if '+threads' in spec:
            if (spec.satisfies('^intel-parallel-studio+tbb')):
                # deal.II/cmake will have hard time picking up TBB from Intel.
                tbb_ver = '.'.join(('%s' % spec['tbb'].version).split('.')[1:])
                options.extend([
                    self.define('TBB_FOUND', True),
                    self.define('TBB_VERSION', tbb_ver),
                    self.define(
                        'TBB_INCLUDE_DIRS',
                        ';'.join(spec['tbb'].headers.directories)
                    ),
                    self.define('TBB_LIBRARIES', spec['tbb'].libs.joined(';'))
                ])
            else:
                options.append(
                    self.define('TBB_DIR', spec['tbb'].prefix)
                )

        # Optional dependencies for which library names are the same as CMake
        # variables:
        for library in (
                'gsl', 'hdf5', 'p4est', 'petsc', 'slepc', 'trilinos', 'metis',
                'sundials', 'nanoflann', 'assimp', 'gmsh', 'muparser',
                'symengine', 'ginkgo'):
            options.append(self.define_from_variant(
                'DEAL_II_WITH_{0}'.format(library.upper()), library
            ))
            if ('+' + library) in spec:
                options.append(self.define(
                    '{0}_DIR'.format(library.upper()), spec[library].prefix
                ))

        # Optional dependencies that do not fit the above pattern:
        # ADOL-C
        options.append(self.define_from_variant(
            'DEAL_II_WITH_ADOLC', 'adol-c'
        ))
        if '+adol-c' in spec:
            options.append(
                self.define('ADOLC_DIR', spec['adol-c'].prefix)
            )

        # ARPACK
        options.append(self.define_from_variant(
            'DEAL_II_WITH_ARPACK', 'arpack'
        ))
        if '+arpack' in spec and '+mpi' in spec:
            options.extend([
                self.define('ARPACK_DIR', spec['arpack-ng'].prefix),
                self.define('DEAL_II_ARPACK_WITH_PARPACK', True)
            ])

        # NetCDF
        # since Netcdf is spread among two, need to do it by hand:
        if '+netcdf' in spec and '+mpi' in spec:
            netcdf_libs = spec['netcdf-cxx'].libs + spec['netcdf-c'].libs
            options.extend([
                self.define('NETCDF_FOUND', True),
                self.define('NETCDF_INCLUDE_DIRS', '{0};{1}'.format(
                    spec['netcdf-cxx'].prefix.include,
                    spec['netcdf-c'].prefix.include
                )),
                self.define('NETCDF_LIBRARIES', netcdf_libs.joined(';'))
            ])
        else:
            options.append(
                self.define('DEAL_II_WITH_NETCDF', False)
            )

        # ScaLAPACK
        options.append(self.define_from_variant(
            'DEAL_II_WITH_SCALAPACK', 'scalapack'
        ))
        if '+scalapack' in spec:
            scalapack_libs = spec['scalapack'].libs
            options.extend([
                self.define('SCALAPACK_FOUND', True),
                self.define(
                    'SCALAPACK_INCLUDE_DIRS', spec['scalapack'].prefix.include
                ),
                self.define('SCALAPACK_LIBRARIES', scalapack_libs.joined(';'))
            ])

        # Open Cascade
        options.append(self.define_from_variant(
            'DEAL_II_WITH_OPENCASCADE', 'oce'
        ))
        if '+oce' in spec:
            options.append(
                self.define('OPENCASCADE_DIR', spec['oce'].prefix)
            )

        # As a final step, collect CXX flags that may have been
        # added anywhere above:
        if len(cxx_flags_release) > 0 and '+optflags' in spec:
            options.extend([
                self.define(
                    'CMAKE_CXX_FLAGS_RELEASE', ' '.join(cxx_flags_release)
                ),
                self.define('CMAKE_CXX_FLAGS', ' '.join(cxx_flags))
            ])

        # Add flags for machine vectorization, used when tutorials
        # and user code is built.
        # See https://github.com/dealii/dealii/issues/9164
        options.append(
            self.define('DEAL_II_CXX_FLAGS', os.environ['SPACK_TARGET_ARGS'])
        )

        return options

    def setup_run_environment(self, env):
        env.set('DEAL_II_DIR', self.prefix)

    def setup_build_environment(self, env):
        spec = self.spec
        if '+cuda' in spec and '+mpi' in spec:
            env.set('CUDAHOSTCXX', spec['mpi'].mpicxx)
