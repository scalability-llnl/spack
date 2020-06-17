# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class ArpackNg(AutotoolsPackage):
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
    url = 'https://github.com/opencollab/arpack-ng/archive/3.3.0.tar.gz'
    git = 'https://github.com/opencollab/arpack-ng.git'

    version('3.3.0', sha256='ad59811e7d79d50b8ba19fd908f92a3683d883597b2c7759fdcc38f6311fe5b3')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Activates MPI support')

    # The function pdlamch10 does not set the return variable.
    # This is fixed upstream
    # see https://github.com/opencollab/arpack-ng/issues/34
    patch('pdlamch10.patch')

    # Fujitsu compiler does not support 'isnan' function.
    # isnan: function that determines whether it is NaN.
    patch('incompatible_isnan_fix.patch', when='%fj')

    depends_on('blas')
    depends_on('lapack')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool@2.4.2:', type='build')

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

    def configure_args(self):
        spec = self.spec
        options = [
            '--with-blas={0}'.format(spec['blas'].libs.ld_flags),
            '--with-lapack={0}'.format(spec['lapack'].libs.ld_flags)
        ]

        if '+shared' not in spec:
            options.append('--enable-shared=no')

        if '+mpi' in spec:
            options.extend([
                '--enable-mpi',
                'F77=%s' % spec['mpi'].mpif77
            ])

        return options
