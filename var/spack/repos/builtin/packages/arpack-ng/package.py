# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ArpackNg(Package):
    """ARPACK-NG is a collection of Fortran77 subroutines designed to solve
    large scale eigenvalue problems.

    Important Features:

    * Reverse Communication Interface.
    * Single and Double Precision Real Arithmetic Versions for Symmetric,
      Non-symmetric, Standard or Generalized Problems.
    * Single and Double Precision Complex Arithmetic Versions for Standard or
      Generalized Problems.
    * Routines for Banded Matrices - Standard or Generalized Problems.
    * Routines for The Singular Value Decomposition.
    * Example driver routines that may be used as templates to implement
      numerous Shift-Invert strategies for all problem types, data types and
      precision.

    This project is a joint project between Debian, Octave and Scilab in order
    to provide a common and maintained version of arpack.

    Indeed, no single release has been published by Rice university for the
    last few years and since many software (Octave, Scilab, R, Matlab...)
    forked it and implemented their own modifications, arpack-ng aims to tackle
    this by providing a common repository and maintained versions.

    arpack-ng is replacing arpack almost everywhere.
    """

    homepage = 'https://github.com/opencollab/arpack-ng'
    url      = 'https://github.com/opencollab/arpack-ng/archive/3.3.0.tar.gz'
    git      = 'https://github.com/opencollab/arpack-ng.git'

    version('develop', branch='master')
    version('3.8.0', sha256='ada5aeb3878874383307239c9235b716a8a170c6d096a6625bfd529844df003d')
    version('3.7.0', sha256='972e3fc3cd0b9d6b5a737c9bf6fd07515c0d6549319d4ffb06970e64fa3cc2d6')
    version('3.6.3', sha256='64f3551e5a2f8497399d82af3076b6a33bf1bc95fc46bbcabe66442db366f453')
    version('3.6.2', sha256='673c8202de996fd3127350725eb1818e534db4e79de56d5dcee8c00768db599a')
    version('3.6.0', sha256='3c88e74cc10bba81dc2c72c4f5fff38a800beebaa0b4c64d321c28c9203b37ea')
    version('3.5.0', sha256='50f7a3e3aec2e08e732a487919262238f8504c3ef927246ec3495617dde81239')
    version('3.4.0', sha256='69e9fa08bacb2475e636da05a6c222b17c67f1ebeab3793762062248dd9d842f')
    version('3.3.0', sha256='ad59811e7d79d50b8ba19fd908f92a3683d883597b2c7759fdcc38f6311fe5b3', deprecated=True)

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Activates MPI support')

    # The function pdlamch10 does not set the return variable.
    # This is fixed upstream
    # see https://github.com/opencollab/arpack-ng/issues/34
    patch('pdlamch10.patch', when='@3.3.0')

    patch('make_install.patch', when='@3.4.0')
    patch('parpack_cmake.patch', when='@3.4.0')

    # Fujitsu compiler does not support 'isnan' function.
    # isnan: function that determines whether it is NaN.
    patch('incompatible_isnan_fix.patch', when='%fj')

    depends_on('blas')
    depends_on('lapack')
    depends_on('automake', when='@3.3.0', type='build')
    depends_on('autoconf', when='@3.3.0', type='build')
    depends_on('libtool@2.4.2:', when='@3.3.0', type='build')
    depends_on('cmake@2.8.6:', when='@3.4.0:', type='build')

    depends_on('mpi', when='+mpi')

    @property
    def libs(self):
        # TODO: do we need spec['arpack-ng:parallel'].libs ?
        # query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libarpack']

        if '+mpi' in self.spec:
            libraries = ['libparpack'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    @when('@:3.7.0 %gcc@10:')
    def setup_build_environment(self, env):
        # version up to and including 3.7.0 are not ported to gcc 10
        # https://github.com/opencollab/arpack-ng/issues/242
        env.set('FFLAGS', '-fallow-argument-mismatch')

    @when('@3.4.0:')
    def install(self, spec, prefix):

        options = ['-DEXAMPLES=ON']
        options.extend(std_cmake_args)
        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        # Make sure we use Spack's blas/lapack:
        lapack_libs = spec['lapack'].libs.joined(';')
        blas_libs = spec['blas'].libs.joined(';')

        options.extend([
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS={0}'.format(spec['lapack'].prefix.include),
            '-DLAPACK_LIBRARIES={0}'.format(lapack_libs),
            '-DBLAS_FOUND=true',
            '-DBLAS_INCLUDE_DIRS={0}'.format(spec['blas'].prefix.include),
            '-DBLAS_LIBRARIES={0}'.format(blas_libs)
        ])

        if '+mpi' in spec:
            options.append('-DMPI=ON')

        # If 64-bit BLAS is used:
        if (spec.satisfies('^openblas+ilp64') or
            spec.satisfies('^intel-mkl+ilp64') or
            spec.satisfies('^intel-parallel-studio+mkl+ilp64')):
            options.append('-DINTERFACE64=1')

        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')

        cmake('.', *options)
        make()
        if self.run_tests:
            make('test')
        make('install')

    @when('@3.3.0')  # noqa
    def install(self, spec, prefix):
        # Apparently autotools are not bootstrapped
        which('libtoolize')()
        bootstrap = Executable('./bootstrap')

        options = ['--prefix=%s' % prefix]

        if '+mpi' in spec:
            options.extend([
                '--enable-mpi',
                'F77=%s' % spec['mpi'].mpif77
            ])

        options.extend([
            '--with-blas={0}'.format(spec['blas'].libs.ld_flags),
            '--with-lapack={0}'.format(spec['lapack'].libs.ld_flags)
        ])
        if '+shared' not in spec:
            options.append('--enable-shared=no')

        bootstrap()
        configure(*options)
        make()
        if self.run_tests:
            make('check')
        make('install')
