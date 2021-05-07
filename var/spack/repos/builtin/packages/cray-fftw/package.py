# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CrayFftw(Package):
    """FFTW is a C subroutine library for computing the discrete Fourier
       transform (DFT) in one or more dimensions, of arbitrary input
       size, and of both real and complex data (as well as of even/odd
       data, i.e. the discrete cosine/sine transforms or DCT/DST).
       This package is a wrapper for Cray's version of FFTW.

       To install this package, list it as an external package in packages.yaml,
       and make sure to load the correct cray-fftw module. In some cases you
       need to load cray-mpich before cray-fftw.
       """

    homepage = "https://docs.nersc.gov/development/libraries/fftw/"
    has_code = False    # Skip attempts to fetch source that is not available

    maintainers = ['haampie']

    version('3.3.8.8')
    version('3.3.8.7')

    provides('fftw-api@3')

    variant(
        'precision', values=any_combination_of(
            'float', 'double'
        ).prohibit_empty_set().with_default('float,double'),
        description='Build the selected floating-point precision libraries'
    )

    variant('openmp', default=False, description="Enable OpenMP support.")
    variant('mpi', default=True, description='Activate MPI support')
    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format('{name} is not installable, you need to specify '
                             'it as an external package in packages.yaml'))

    @property
    def libs(self):

        # Reduce repetitions of entries
        query_parameters = list(llnl.util.lang.dedupe(
            self.spec.last_query.extra_parameters
        ))

        # List of all the suffixes associated with float precisions
        precisions = [
            ('float', 'f'),
            ('double', ''),
        ]

        # Retrieve the correct suffixes, or use double as a default
        suffixes = [v for k, v in precisions if k in query_parameters] or ['']

        # Construct the list of libraries that needs to be found
        libraries = []
        for sfx in suffixes:
            if 'mpi' in query_parameters and '+mpi' in self.spec:
                libraries.append('libfftw3' + sfx + '_mpi')

            if 'openmp' in query_parameters and '+openmp' in self.spec:
                libraries.append('libfftw3' + sfx + '_omp')

            libraries.append('libfftw3' + sfx)

        return find_libraries(libraries, root=self.prefix, recursive=True)
