# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Elk(MakefilePackage):
    """An all-electron full-potential linearised augmented-plane wave
    (FP-LAPW) code with many advanced features."""

    homepage = 'http://elk.sourceforge.net/'
    url      = 'https://sourceforge.net/projects/elk/files/elk-3.3.17.tgz'

    version('3.3.17', sha256='c9b87ae4ef367ed43afc2d43eb961745668e40670995e8e24c13db41b7e85d73')

    # Elk provides these libraries, but allows you to specify your own
    variant('blas',   default=True,
            description='Build with custom BLAS library')
    variant('lapack', default=True,
            description='Build with custom LAPACK library')
    variant('fft',    default=True,
            description='Build with custom FFT library')

    # Elk does not provide these libraries, but allows you to use them
    variant('mpi',    default=True,
            description='Enable MPI parallelism')
    variant('openmp', default=True,
            description='Enable OpenMP support')
    variant('libxc',  default=True,
            description='Link to Libxc functional library')

    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('fftw',   when='+fft')
    depends_on('mpi@2:', when='+mpi')
    depends_on('libxc',  when='+libxc')

    # Cannot be built in parallel
    parallel = False

    def edit(self, spec, prefix):
        # Dictionary of configuration options
        config = {
            'MAKE': 'make',
            'AR':   'ar'
        }

        # Compiler-specific flags
        flags = ''
        if self.compiler.name == 'intel':
            flags = '-O3 -ip -unroll -no-prec-div'
        elif self.compiler.name == 'gcc':
            flags = '-O3 -ffast-math -funroll-loops'
        elif self.compiler.name == 'pgi':
            flags = '-O3 -lpthread'
        elif self.compiler.name == 'g95':
            flags = '-O3 -fno-second-underscore'
        elif self.compiler.name == 'nag':
            flags = '-O4 -kind=byte -dusty -dcfuns'
        elif self.compiler.name == 'xl':
            flags = '-O3'
        config['F90_OPTS'] = flags
        config['F77_OPTS'] = flags

        # BLAS/LAPACK support
        # Note: BLAS/LAPACK must be compiled with OpenMP support
        # if the +openmp variant is chosen
        blas = 'blas.a'
        lapack = 'lapack.a'
        if '+blas' in spec:
            blas = spec['blas'].libs.joined()
        if '+lapack' in spec:
            lapack = spec['lapack'].libs.joined()
        # lapack must come before blas
        config['LIB_LPK'] = ' '.join([lapack, blas])

        # FFT support
        if '+fft' in spec:
            config['LIB_FFT'] = join_path(spec['fftw'].prefix.lib,
                                          'libfftw3.so')
            config['SRC_FFT'] = 'zfftifc_fftw.f90'
        else:
            config['LIB_FFT'] = 'fftlib.a'
            config['SRC_FFT'] = 'zfftifc.f90'

        # MPI support
        if '+mpi' in spec:
            config['F90'] = spec['mpi'].mpifc
            config['F77'] = spec['mpi'].mpif77
        else:
            config['F90'] = spack_fc
            config['F77'] = spack_f77
            config['SRC_MPI'] = 'mpi_stub.f90'

        # OpenMP support
        if '+openmp' in spec:
            config['F90_OPTS'] += ' ' + self.compiler.openmp_flag
            config['F77_OPTS'] += ' ' + self.compiler.openmp_flag
        else:
            config['SRC_OMP'] = 'omp_stub.f90'

        # Libxc support
        if '+libxc' in spec:
            config['LIB_libxc'] = ' '.join([
                join_path(spec['libxc'].prefix.lib, 'libxcf90.so'),
                join_path(spec['libxc'].prefix.lib, 'libxc.so')
            ])
            config['SRC_libxc'] = ' '.join([
                'libxc_funcs.f90',
                'libxc.f90',
                'libxcifc.f90'
            ])
        else:
            config['SRC_libxc'] = 'libxcifc_stub.f90'

        # Write configuration options to include file
        with open('make.inc', 'w') as inc:
            for key in config:
                inc.write('{0} = {1}\n'.format(key, config[key]))

    def install(self, spec, prefix):
        # The Elk Makefile does not provide an install target
        mkdir(prefix.bin)

        install('src/elk',                   prefix.bin)
        install('src/eos/eos',               prefix.bin)
        install('src/spacegroup/spacegroup', prefix.bin)

        install_tree('examples', join_path(prefix, 'examples'))
        install_tree('species',  join_path(prefix, 'species'))
