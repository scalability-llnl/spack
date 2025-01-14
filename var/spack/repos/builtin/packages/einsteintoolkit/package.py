# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from spack import *


class Einsteintoolkit(AutotoolsPackage):
    """The Einstein Toolkit is a community-driven software platform of core
    computational tools to advance and support research in relativistic
    astrophysics and gravitational physics."""

    homepage = 'https://einsteintoolkit.org/index.html'
    git      = 'https://bitbucket.org/cactuscode/cactus.git'

    maintainers = ['eschnett']

    version('2021.5.0', tag='ET_2021_05_v0', commit='346f9fee3de09fc1c3f020e9eedca7edf833d561')
    version('2021.11.0', tag='ET_2021_11_v0', commit='83314864d6329b09401b1d653050fd9cc5cdc35f')

    variant('blas', default=True, description='Enable BLAS')
    variant('debug', default=False, description='Build in debug mode')
    variant('fftw', default=True, description='Enable FFTW')
    variant('gsl', default=True, description='Enable GSL')
    variant('hdf5', default=True, description='Enable HDF5')
    variant('hwloc', default=True, description='Enable hwloc')
    variant('lapack', default=True, description='Enable LAPACK')
    variant('libjpeg', default=True, description='Enable libjpeg')
    variant('lorene', default=True, description='Enable LORENE')
    variant('mpi', default=True, description='Enable MPI')
    variant('opencl', default=False, description='Enable OpenCL')
    variant('openmp', default=True, description='Enable OpenMP')
    variant('openssl', default=True, description='Enable OpenSSL')
    variant('papi', default=False, description='Enable PAPI')
    variant('petsc', default=False, description='Enable PETSc')
    variant('pthreads', default=True, description='Enable pthreads')
    variant('zlib', default=True, description='Enable zlib')

    # These dependencies would be needed to re-run autoconf
    # depends_on('autoconf @2.13', type='build')
    # depends_on('automake', type='build')  # not actually needed, but required by Spack
    # depends_on('libtool', type='build')   # not actually needed, but required by Spack
    # depends_on('m4', type='build')

    # These dependencies can be added, if necessary
    # depends_on('awk', type='build')
    # depends_on('git', type='build')
    # depends_on('patch', type='build')
    # depends_on('perl', type='build')
    # depends_on('python')
    # depends_on('tar', type='build')

    depends_on('blas', when='+blas')
    depends_on('fftw @3', when='+fftw')
    depends_on('gsl', when='+gsl')
    depends_on('hdf5 +cxx +fortran +hl', when='+hdf5')
    depends_on('hdf5 +mpi', when='+hdf5 +mpi')
    depends_on('hwloc', when='+hwloc')
    depends_on('lapack', when='+lapack')
    depends_on('jpeg', when='+libjpeg')   # Could be generic 'libjpeg'
    depends_on('lorene', when='+lorene')
    depends_on('mpi', when='+mpi')
    depends_on('opencl', when='+opencl')
    depends_on('openssl', when='+openssl')
    depends_on('papi', when='+papi')
    depends_on('petsc', when='+petsc')
    depends_on('zlib', when='+zlib')

    # Define resources for arrangements and thorns

    for (version, tag) in [
        ('2021.5.0', 'ET_2021_05_v0'),
        ('2021.11.0', 'ET_2021_11_v0'),
    ]:

        resource(
            when='@' + version,
            name='manifest',
            git='https://bitbucket.org/einsteintoolkit/manifest.git',
            tag=tag,
            # destination='repos'
            destination='.'
        )

        resource(
            when='@' + version,
            name='simfactory2',
            git='https://bitbucket.org/simfactory/simfactory2.git',
            tag=tag,
            # destination='repos'
            destination='.',
            placement='simfactory'
        )

        resource(
            when='@' + version,
            name='einsteinexamples',
            git='https://bitbucket.org/einsteintoolkit/einsteinexamples.git',
            tag=tag,
            destination='.',
            placement='par'
        )

        resource(
            when='@' + version,
            name='utilities',
            git='https://bitbucket.org/cactuscode/utilities.git',
            tag=tag,
            destination='.',
            placement='utils'
        )

        resource(
            when='@' + version,
            name='coredoc',
            git='https://bitbucket.org/cactuscode/coredoc.git',
            tag=tag,
            destination='.',
            placement='CoreDoc'
        )

        resource(
            when='@' + version,
            name='cactusbase',
            git='https://bitbucket.org/cactuscode/cactusbase.git',
            tag=tag,
            destination='arrangements',
            placement='CactusBase'
        )

        resource(
            when='@' + version,
            name='cactusconnect',
            git='https://bitbucket.org/cactuscode/cactusconnect.git',
            tag=tag,
            destination='arrangements',
            placement='CactusConnect'
        )

        resource(
            when='@' + version,
            name='cactuselliptic',
            git='https://bitbucket.org/cactuscode/cactuselliptic.git',
            tag=tag,
            destination='arrangements',
            placement='CactusElliptic'
        )

        resource(
            when='@' + version,
            name='cactusexamples',
            git='https://bitbucket.org/cactuscode/cactusexamples.git',
            tag=tag,
            destination='arrangements',
            placement='CactusExamples'
        )

        resource(
            when='@' + version,
            name='cactusio',
            git='https://bitbucket.org/cactuscode/cactusio.git',
            tag=tag,
            destination='arrangements',
            placement='CactusIO'
        )

        resource(
            when='@' + version,
            name='cactusnumerical',
            git='https://bitbucket.org/cactuscode/cactusnumerical.git',
            tag=tag,
            destination='arrangements',
            placement='CactusNumerical'
        )

        resource(
            when='@' + version,
            name='cactuspugh',
            git='https://bitbucket.org/cactuscode/cactuspugh.git',
            tag=tag,
            destination='arrangements',
            placement='CactusPUGH'
        )

        resource(
            when='@' + version,
            name='cactuspughio',
            git='https://bitbucket.org/cactuscode/cactuspughio.git',
            tag=tag,
            destination='arrangements',
            placement='CactusPUGHIO'
        )

        resource(
            when='@' + version,
            name='cactustest',
            git='https://bitbucket.org/cactuscode/cactustest.git',
            tag=tag,
            destination='arrangements',
            placement='CactusTest'
        )

        resource(
            when='@' + version,
            name='cactusutils',
            git='https://bitbucket.org/cactuscode/cactusutils.git',
            tag=tag,
            destination='arrangements',
            placement='CactusUtils'
        )

        resource(
            when='@' + version,
            name='cactuswave',
            git='https://bitbucket.org/cactuscode/cactuswave.git',
            tag=tag,
            destination='arrangements',
            placement='CactusWave'
        )

        resource(
            when='@' + version,
            name='carpet',
            git='https://bitbucket.org/eschnett/carpet.git',
            tag=tag,
            destination='arrangements',
            placement='Carpet'
        )

        resource(
            when='@' + version,
            name='ctthorns',
            git='https://bitbucket.org/eloisa/ctthorns.git',
            tag=tag,
            destination='arrangements',
            placement='CTThorns'
        )

        resource(
            when='@' + version,
            name='einsteinanalysis',
            git='https://bitbucket.org/einsteintoolkit/einsteinanalysis.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinAnalysis'
        )

        resource(
            when='@' + version,
            name='einsteinbase',
            git='https://bitbucket.org/einsteintoolkit/einsteinbase.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinBase'
        )

        resource(
            when='@' + version,
            name='einsteineos',
            git='https://bitbucket.org/einsteintoolkit/einsteineos.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinEOS'
        )

        resource(
            when='@' + version,
            name='einsteinevolve',
            git='https://bitbucket.org/einsteintoolkit/einsteinevolve.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinEvolve'
        )

        resource(
            when='@' + version,
            name='einsteinexact',
            git='https://github.com/barrywardell/EinsteinExact.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinExact'
        )

        resource(
            when='@' + version,
            name='einsteininitialdata',
            git='https://bitbucket.org/einsteintoolkit/einsteininitialdata.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinInitialData'
        )

        # NRPyPN

        resource(
            when='@' + version,
            name='einsteinutils',
            git='https://bitbucket.org/einsteintoolkit/einsteinutils.git',
            tag=tag,
            destination='arrangements',
            placement='EinsteinUtils'
        )

        resource(
            when='@' + version + ' +blas',
            name='BLAS',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-BLAS.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='BLAS'
        )

        resource(
            when='@' + version + ' +fftw',
            name='FFTW3',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-FFTW3.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='FFTW3'
        )

        resource(
            when='@' + version + ' +gsl',
            name='GSL',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-GSL.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='GSL'
        )

        resource(
            when='@' + version + ' +hdf5',
            name='HDF5',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-HDF5.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='HDF5'
        )

        resource(
            when='@' + version + ' +hwloc',
            name='hwloc',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-hwloc.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='hwloc'
        )

        resource(
            when='@' + version + ' +lapack',
            name='lapack',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-LAPACK.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='LAPACK'
        )

        resource(
            when='@' + version + ' +libjpeg',
            name='libjpeg',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-libjpeg.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='libjpeg'
        )

        resource(
            when='@' + version + ' +lorene',
            name='LORENE',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-LORENE.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='LORENE'
        )

        resource(
            when='@' + version + ' +mpi',
            name='MPI',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-MPI.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='MPI'
        )

        # OpenBLAS is not needed; we can use BLAS and LAPACK instead

        resource(
            when='@' + version + ' +opencl',
            name='OpenCL',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-OpenCL.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='OpenCL'
        )

        resource(
            when='@' + version + ' +openssl',
            name='OpenSSL',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-OpenSSL.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='OpenSSL'
        )

        resource(
            when='@' + version + ' +papi',
            name='PAPI',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-PAPI.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='PAPI'
        )

        resource(
            when='@' + version + ' +petsc',
            name='PETSc',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-PETSc.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='PETSc'
        )

        # 'pciutils' is probably unused

        resource(
            when='@' + version + ' +pthreads',
            name='pthreads',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-pthreads.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='pthreads'
        )

        resource(
            when='@' + version + ' +zlib',
            name='zlib',
            svn='https://github.com/EinsteinToolkit/ExternalLibraries-zlib.git/tags/' + tag,
            destination=join_path('arrangements', 'ExternalLibraries'),
            placement='zlib'
        )

        resource(
            when='@' + version,
            name='Kranc',
            git='https://github.com/ianhinder/Kranc.git',
            tag=tag,
            destination='arrangements',
            placement={'Auxiliary/Cactus/KrancNumericalTools': 'KrancNumericalTools'}
        )

        resource(
            when='@' + version,
            name='lean',
            git='https://bitbucket.org/canuda/lean_public.git',
            tag=tag,
            destination='arrangements',
            placement='Lean'
        )

        resource(
            when='@' + version,
            name='llama',
            git='https://bitbucket.org/llamacode/llama.git',
            tag=tag,
            destination='arrangements',
            placement='Llama'
        )

        resource(
            when='@' + version,
            name='mclachlan',
            git='https://bitbucket.org/einsteintoolkit/mclachlan.git',
            tag=tag,
            destination='arrangements',
            placement='McLachlan'
        )

        resource(
            when='@' + version,
            name='numerical',
            git='https://bitbucket.org/cactuscode/numerical.git',
            tag=tag,
            destination='arrangements',
            placement='Numerical'
        )

        resource(
            when='@' + version,
            name='pittnullcode',
            git='https://bitbucket.org/einsteintoolkit/pittnullcode.git',
            tag=tag,
            destination='arrangements',
            placement='PITTNullCode'
        )

        # Not checked out: Power

        resource(
            when='@' + version,
            name='Proca',
            git='https://bitbucket.org/canuda/Proca.git',
            tag=tag,
            destination='arrangements'
        )

        resource(
            when='@' + version,
            name='wvuthorns',
            git='https://bitbucket.org/zach_etienne/wvuthorns.git',
            tag=tag,
            destination='arrangements',
            placement='WVUThorns'
        )

        resource(
            when='@' + version,
            name='wvuthorns_diagnostics',
            git='https://bitbucket.org/zach_etienne/wvuthorns_diagnostics.git',
            tag=tag,
            destination='arrangements',
            placement='WVUThorns_Diagnostics'
        )

    configure_directory = join_path('lib', 'make')
    build_directory = '.'

    def autoreconf(self, spec, prefix):
        # with working_dir(join_path('lib', 'make')):
        #     autoconf()
        pass

    def _symlink_repo(self, source_path, dest_path, thorns):
        mkdirp(dest_path)
        for thorn in thorns:
            os.symlink(join_path(source_path, thorn), join_path(dest_path, thorn))

    def configure(self, spec, prefix):
        self_path = os.path.dirname(inspect.getmodule(self).__file__)

        copy(join_path(self_path, 'cpp.sh'), 'cpp.sh')

        options = [
            'CPP = cpp',
            'CC = ' + self.compiler.cc_names[0],
            'CXX = ' + self.compiler.cxx_names[0],
            'FPP = ' + join_path(self.stage.source_path, 'cpp.sh'),
            'FC = ' + self.compiler.fc_names[0],
            'F90 = ' + self.compiler.fc_names[0],

            'CPPFLAGS = -D_XOPEN_SOURCE -D_XOPEN_SOURCE_EXTENDED',
            'CFLAGS = -g ' + self.compiler.c11_flag,
            'CXXFLAGS = -g ' + self.compiler.cxx17_flag,
            'FPPFLAGS =',
            'F90FLAGS = -g -fcray-pointer -ffixed-line-length-none',

            'C_LINE_DIRECTIVES = yes',
            'F_LINE_DIRECTIVES = yes',

            'DEBUG = ' + ('yes' if '+debug' in spec else 'no'),
            'CPP_DEBUG_FLAGS =',
            'C_DEBUG_FLAGS = -fbounds-check -fstack-protector-all -ftrapv',
            'CXX_DEBUG_FLAGS = -fbounds-check -fstack-protector-all -ftrapv',
            'FPP_DEBUG_FLAGS =',
            ('F90_DEBUG_FLAGS = '
             '-fcheck=bounds,do,mem,pointer,recursion -finit-character=65 '
             '-finit-integer=42424242 -finit-real=nan -fstack-protector-all -ftrapv'),

            'OPTIMISE = ' + ('no' if '+debug' in spec else 'yes'),
            ('C_OPTIMISE_FLAGS = '
             '-O3 -fcx-limited-range -fexcess-precision=fast -fno-math-errno '
             '-fno-rounding-math -fno-signaling-nans -funsafe-math-optimizations'),
            ('CXX_OPTIMISE_FLAGS = '
             '-O3 -fcx-limited-range -fexcess-precision=fast -fno-math-errno '
             '-fno-rounding-math -fno-signaling-nans -funsafe-math-optimizations'),
            ('F90_OPTIMISE_FLAGS = '
             '-O3 -fcx-limited-range -fexcess-precision=fast -fno-math-errno '
             '-fno-rounding-math -fno-signaling-nans -funsafe-math-optimizations'),

            'OPENMP = ' + ('yes' if '+openmp' in spec else 'no'),
            'CPP_OPENMP_FLAGS = ' + self.compiler.openmp_flag,
            'FPP_OPENMP_FLAGS = -D_OPENMP',

            'WARN = yes',

            # CactusUtils/Vectors self-tests fail: A call to `vec_loadu_maybe` is
            # compiled to the instruction `movapd`, which looks very wrong. If so,
            # this would point to a bug in the compiler.
            'VECTORISE = yes',
            'VECTORISE_ALWAYS_USE_UNALIGNED_LOADS = yes',
            'VECTORISE_INLINE = yes',
        ]

        if '+blas' in spec:
            options.extend([
                'BLAS_DIR = ' + spec['blas'].prefix,
                'BLAS_LIBS = ' + ' '.join(spec['blas'].libs.names),
            ])
        if '+fftw' in spec:
            options.append('FFTW3_DIR = ' + spec['fftw'].prefix)
        if '+gsl' in spec:
            options.append('GSL_DIR = ' + spec['gsl'].prefix)
        if '+hdf5' in spec:
            options.extend([
                'HDF5_DIR = ' + spec['hdf5'].prefix,
                'HDF5_ENABLE_CXX = yes',
                'HDF5_ENABLE_FORTRAN = yes',
                'HDF5_INC_DIRS = ' + spec['hdf5'].prefix.include,
                'HDF5_LIB_DIRS = ' + spec['hdf5'].prefix.lib,
                ('HDF5_LIBS = '
                 'hdf5_hl_cpp hdf5_cpp hdf5_hl_f90cstub hdf5_f90cstub '
                 'hdf5_hl_fortran hdf5_fortran hdf5_hl hdf5'),
            ])
        if '+hwloc' in spec:
            options.append('HWLOC_DIR = ' + spec['hwloc'].prefix)
        if '+lapack' in spec:
            options.extend([
                'LAPACK_DIR = ' + spec['lapack'].prefix,
                'LAPACK_LIBS = ' + ' '.join(spec['lapack'].libs.names),
            ])
        if '+jpeg' in spec:
            options.append('LIBJPEG_DIR = ' + spec['jpeg'].prefix)
        if '+lorene' in spec:
            options.append('LORENE_DIR = ' + spec['lorene'].prefix)
        if '+mpi' in spec:
            options.extend([
                'MPI_DIR = ' + spec['mpi'].prefix,
                'MPI_INC_DIRS = ' + spec['mpi'].prefix.include,
                'MPI_LIB_DIRS = ' + spec['mpi'].prefix.lib,
                'MPI_LIBS = mpi',
            ])

        if '+opencl' in spec:
            options.append('OPENCL_DIR = ' + spec['opencl'].prefix)
        if '+openssl' in spec:
            options.append('OPENSSL_DIR = ' + spec['openssl'].prefix)
        if '+papi' in spec:
            options.append('PAPI_DIR = ' + spec['papi'].prefix)
        if '+petsc' in spec:
            options.extend([
                'PETSC_DIR = ' + spec['petsc'].prefix,
                'PETSC_ARCH_LIBS = m',
            ])
        if '+pthreads' in spec:
            options.append('PTHREADS_DIR = NO_BUILD')
        if '+zlib' in spec:
            options.append('ZLIB_DIR = ' + spec['zlib'].prefix)

        with open('options.cfg', 'w') as opt:
            for var in options:
                opt.write('{0}\n'.format(var))

        # We should instead download a current thorn list
        copy(join_path(self_path, 'thornlist.th'), 'thornlist.th')

    def build(self, spec, prefix):
        # sim = Executable(join_path('simfactory', 'bin', 'sim'))
        # sim('build')

        with working_dir(self.build_directory):
            configureopts = [
                'PROMPT=no',               # non-interactive
                'THORNLIST=thornlist.th',  # list of thorns (plug-ins)
                'options=options.cfg',     # build options
            ]
            makeopts = [
                'VERBOSE=yes',
            ]
            make('sim-config', *(configureopts + makeopts))
            make('sim-utils', *makeopts)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install_tree('exe', prefix.bin)
            mkdirp(join_path(prefix, 'doc'))
            install(join_path('doc', '*.pdf'), join_path(prefix, 'doc'))
            mkdirp(join_path(prefix, 'par'))
            install_tree(join_path('par', '*'), join_path(prefix, 'par'))
