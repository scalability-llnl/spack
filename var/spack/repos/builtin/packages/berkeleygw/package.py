# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Berkeleygw(MakefilePackage):
    """BerkeleyGW is a many-body perturbation theory code for excited states,
    using the GW method and the GW plus Bethe-Salpeter equation (GW-BSE) method
    to solve respectively for quasiparticle excitations and optical properties of
    materials."""

    homepage = "https://berkeleygw.org"

    version('2.1',
            '31f3b643dd937350c3866338321d675d4a1b1f54c730b43ad74ae67e75a9e6f2',
            url='https://berkeley.box.com/shared/static/ze3azi5vlyw7hpwvl9i5f82kaiid6g0x.gz',
            expand=False)

    variant('mpi', default=True, description='Builds with MPI support')
    variant('elpa', default=True, description='Build with ELPA support')
    variant('python', default=False, description='Build with Python support')
    variant('openmp', default=True, description='Build with OpenMP support')
    variant('scalapack', default=True, description='Build with ScaLAPACK support')
    variant('hdf5', default=True, description='Builds with HDF5 support')
    variant('debug', default=False, description='Builds with DEBUG flag')
    variant('verbose', default=False, description='Builds with VERBOSE flag')

    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5+fortran+hl', when='+hdf5~mpi')
    depends_on('hdf5+fortran+hl+mpi', when='+hdf5+mpi')
    depends_on('scalapack', when='+scalapack+mpi')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('fftw-api@3+openmp', when='+openmp')
    depends_on('fftw-api@3~openmp', when='~openmp')

    depends_on('python@:2', type=('build', 'run'), when='+python')
    depends_on('py-numpy@:1.16', type=('build', 'run'), when='+python')
    depends_on('py-setuptools@:44', type=('build', 'run'), when='+python')
    depends_on('py-h5py@:2', type=('build', 'run'), when='+hdf5+python')

    depends_on('perl', type='test')

    conflicts(
        '+scalapack',
        when='~mpi',
        msg='scalapack is a parallel library and needs MPI support'
    )

    conflicts(
        '+elpa',
        when='~mpi',
        msg='elpa is a parallel library and needs MPI support'
    )

    # the concretizer is selecting non threaded versions of fftw and openblas even though +openmp is set...
    # as a workaround, the conflicts below force the user to spec ^fftw+openmp ^openblas threads=openmp
    # but this may also happen for other providers of fftw and blas...
    conflicts('^fftw~openmp', when='+openmp')
    conflicts('^openblas threads=none', when='+openmp')
    conflicts('^openblas threads=pthreads', when='+openmp')

    parallel = False

    def edit(self, spec, prefix):
        # archive is a tar file, despite the .gz expension
        tar = which('tar')
        tar('-x', '-f', self.stage.archive_file, '--strip-components=1')

        # get generic arch.mk template
        copy(join_path(self.stage.source_path, 'config', 'generic.mpi.linux.mk'),
             'arch.mk')

        # don't try to install missing file
        filter_file('install manual.html', '#install manual.html', 'Makefile')

        # don't rebuild in the install and test steps
        filter_file('install: all', 'install:', 'Makefile')
        filter_file('check: all', 'check:', 'Makefile')

        # use parallelization in tests
        filter_file(r'cd testsuite \&\& \$\(MAKE\) check$',
                    'cd testsuite && $(MAKE) check-parallel',
                    'Makefile')

        # remove stack ulimit in order to run openmp tests
        filter_file(r'function run_testsuite\(\) {',
                    'function run_testsuite() {\nulimit -s unlimited',
                    'testsuite/run_testsuite.sh')

    def setup_build_environment(self, env):
        if self.run_tests:
            env.set('OMP_NUM_THREADS', '2')
            env.set('BGW_TEST_MPI_NPROCS', '2')

    def build(self, spec, prefix):

        buildopts = []
        paraflags = []

        if '+mpi' in spec:
            paraflags.append('-DMPI')

        if '+openmp' in spec:
            paraflags.append('-DOMP')
            spec.compiler_flags['fflags'].append(self.compiler.openmp_flag)

        buildopts.append('C_PARAFLAG=-DPARA')
        buildopts.append('PARAFLAG=%s' % ' '.join(paraflags))

        debugflag = ""
        if '+debug' in spec:
            debugflag += "-DDEBUG "
        if '+verbose' in spec:
            debugflag += "-DVERBOSE "
        buildopts.append('DEBUGFLAG=%s' % debugflag)

        buildopts.append('LINK=%s' % spec['mpi'].mpifc)
        buildopts.append('C_LINK=%s' % spec['mpi'].mpicxx)

        buildopts.append('FOPTS=%s' % ' '.join(spec.compiler_flags['fflags']))
        buildopts.append('C_OPTS=%s' % ' '.join(spec.compiler_flags['cflags']))

        mathflags = []

        mathflags.append('-DUSEFFTW3')
        buildopts.append('FFTWINCLUDE=%s' % spec['fftw-api'].prefix.include)
        fftwspec = spec['fftw-api:openmp' if '+openmp' in spec else 'fftw-api']
        buildopts.append('FFTWLIB=%s' % fftwspec.libs.ld_flags)

        buildopts.append('LAPACKLIB=%s' % spec['lapack'].libs.ld_flags)

        if '+scalapack' in spec:
            mathflags.append('-DUSESCALAPACK')
            buildopts.append('SCALAPACKLIB=%s' % spec['scalapack'].libs.ld_flags)

        if spec.satisfies('%intel'):
            buildopts.append('COMPFLAG=-DINTEL')
            buildopts.append('MOD_OPT=-module ')
            buildopts.append('F90free=%s -free' % spec['mpi'].mpifc)
            buildopts.append('FCPP=cpp -C -P -ffreestanding')
            buildopts.append('C_COMP=%s' % spec['mpi'].mpicc)
            buildopts.append('CC_COMP=%s' % spec['mpi'].mpicxx)
            buildopts.append('BLACSDIR=%s' % spec['scalapack'].libs)
            buildopts.append('BLACS=%s' % spec['scalapack'].libs.ld_flags)
            buildopts.append('FOPTS=%s' % ' '.join(spec.compiler_flags['fflags']))
        elif spec.satisfies('%gcc'):
            c_flags = '-std=c99'
            cxx_flags = '-std=c++0x'
            f90_flags = "-ffree-form -ffree-line-length-none -fno-second-underscore"
            if spec.satisfies('%gcc@10:'):
                c_flags += ' -fcommon'
                cxx_flags += ' -fcommon'
                f90_flags += ' -fallow-argument-mismatch'
            buildopts.append('COMPFLAG=-DGNU')
            buildopts.append('MOD_OPT=-J ')
            buildopts.append('F90free=%s %s' % (spec['mpi'].mpifc, f90_flags))
            buildopts.append('FCPP=cpp -C -nostdinc')
            buildopts.append('C_COMP=%s %s' % (spec['mpi'].mpicc, c_flags))
            buildopts.append('CC_COMP=%s %s' % (spec['mpi'].mpicxx, cxx_flags))
            buildopts.append('FOPTS=%s' % ' '.join(spec.compiler_flags['fflags']))
        elif spec.satisfies('%fj'):
            c_flags = '-std=c99'
            cxx_flags = '-std=c++0x'
            f90_flags = "-Free"
            buildopts.append('COMPFLAG=')
            buildopts.append('MOD_OPT=-module ')
            buildopts.append('F90free=%s %s' % (spec['mpi'].mpifc, f90_flags))
            buildopts.append('FCPP=cpp -C -nostdinc')
            buildopts.append('C_COMP=%s %s' % (spec['mpi'].mpicc, c_flags))
            buildopts.append('CC_COMP=%s %s' % (spec['mpi'].mpicxx, cxx_flags))
            buildopts.append('FOPTS=-Kfast -Knotemparraystack %s' % ' '.join(spec.compiler_flags['fflags']))
        else:
            raise InstallError("Spack does not yet have support for building "
                               "BerkeleyGW with compiler %s" % spec.compiler)

        if '+hdf5' in spec:
            mathflags.append('-DHDF5')
            buildopts.append('HDF5INCLUDE=%s' % spec['hdf5'].prefix.include)
            buildopts.append('HDF5LIB=%s' % spec['hdf5:hl,fortran'].libs.ld_flags)

        if '+elpa' in spec:
            mathflags.append('-DUSEELPA')
            elpa = spec['elpa']

            if '+openmp' in spec:
                elpa_suffix = '_openmp'
            else:
                elpa_suffix = ''

            elpa_incdir = elpa.headers.directories[0]
            elpa_libs = join_path(elpa.libs.directories[0],
                                  'libelpa%s.%s' % (elpa_suffix, dso_suffix))

            buildopts.append('ELPALIB=%s' % elpa_libs)
            buildopts.append('ELPAINCLUDE=%s' % join_path(elpa_incdir, 'modules'))

        buildopts.append('MATHFLAG=%s' % ' '.join(mathflags))

        make('all-flavors', *buildopts)

    def install(self, spec, prefix):
        make('install', 'INSTDIR=%s' % prefix)
