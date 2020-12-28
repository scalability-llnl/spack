# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Chombo(MakefilePackage):
    """The Chombo package provides a set of tools for implementing finite
       difference and finite-volume methods for the solution of partial
       differential equations on block-structured adaptively refined
       logically rectangular (i.e. Cartesian) grids."""

    homepage = "https://commons.lbl.gov/display/chombo"
    git      = "http://bitbucket.org/drhansj/chombo-xsdk.git"

    tags = ['ecp', 'ecp-apps']

    # Use whatever path Brian V. and Terry L. agreed upon, but preserve version
    version('3.2', commit='71d856c')
    version('develop', tag='master')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('hdf5', default=True, description='Enable HDF5 support')
    variant('dims', default='3', values=('1', '2', '3', '4', '5', '6'),
            multi=False, description='Number of PDE dimensions [1-6]')

    patch('hdf5-16api.patch', when='@3.2', level=0)
    patch('Make.defs.local.template.patch', when='@3.2', level=0)

    depends_on('blas')
    depends_on('lapack')
    depends_on('gmake', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5+mpi', when='+mpi+hdf5')

    def edit(self, spec, prefix):

        # Set fortran name mangling in Make.defs
        defs_file = FileFilter('./lib/mk/Make.defs')
        defs_file.filter(r'^\s*#\s*cppcallsfort\s*=\s*',
                         'cppcallsfort = -DCH_FORT_UNDERSCORE')

        # Set remaining variables in Make.defs.local
        # Make.defs.local.template.patch ensures lines for USE_TIMER,
        # USE_LAPACK and lapackincflags are present
        copy('./lib/mk/Make.defs.local.template',
             './lib/mk/Make.defs.local')

        defs_file = FileFilter('./lib/mk/Make.defs.local')

        # Unconditional settings
        defs_file.filter(r'^\s*#\s*DEBUG\s*=\s*', 'DEBUG = FALSE')
        defs_file.filter(r'^\s*#\s*OPT\s*=\s*', 'OPT = TRUE')
        defs_file.filter(r'^\s*#\s*PIC\s*=\s*', 'PIC = TRUE')
        # timer code frequently fails compiles. So disable it.
        defs_file.filter(r'^\s*#\s*USE_TIMER\s*=\s*', 'USE_TIMER = FALSE')

        # LAPACK setup
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        defs_file.filter(r'^\s*#\s*USE_LAPACK\s*=\s*', 'USE_LAPACK = TRUE')
        defs_file.filter(
            r'^\s*#\s*lapackincflags\s*=\s*',
            'lapackincflags = -I%s' % spec['lapack'].prefix.include)
        defs_file.filter(
            r'^\s*#\s*syslibflags\s*=\s*',
            'syslibflags = %s' % lapack_blas.ld_flags)

        # Compilers and Compiler flags
        defs_file.filter(r'^\s*#\s*CXX\s*=\s*', 'CXX = %s' % spack_cxx)
        defs_file.filter(r'^\s*#\s*FC\s*=\s*', 'FC = %s' % spack_fc)
        if '+mpi' in spec:
            defs_file.filter(
                r'^\s*#\s*MPICXX\s*=\s*',
                'MPICXX = %s' % self.spec['mpi'].mpicxx)

        # Conditionally determined settings
        defs_file.filter(
            r'^\s*#\s*MPI\s*=\s*',
            'MPI = %s' % ('TRUE' if '+mpi' in spec else 'FALSE'))
        defs_file.filter(
            r'^\s*#\s*DIM\s*=\s*',
            'DIM = %s' % spec.variants['dims'].value)

        # HDF5 settings
        if '+hdf5' in spec:
            defs_file.filter(r'^\s*#\s*USE_HDF5\s*=\s*', 'USE_HDF5 = TRUE')
            defs_file.filter(
                r'^\s*#\s*HDFINCFLAGS\s*=.*',
                'HDFINCFLAGS = -I%s' % spec['hdf5'].prefix.include)
            defs_file.filter(
                r'^\s*#\s*HDFLIBFLAGS\s*=.*',
                'HDFLIBFLAGS = %s' % spec['hdf5'].libs.ld_flags)
            if '+mpi' in spec:
                defs_file.filter(
                    r'^\s*#\s*HDFMPIINCFLAGS\s*=.*',
                    'HDFMPIINCFLAGS = -I%s' % spec['hdf5'].prefix.include)
                defs_file.filter(
                    r'^\s*#\s*HDFMPILIBFLAGS\s*=.*',
                    'HDFMPILIBFLAGS = %s' % spec['hdf5'].libs.ld_flags)

    def build(self, spec, prefix):
        with working_dir('lib'):
            gmake('all')

    def install(self, spec, prefix):
        with working_dir('lib'):
            install_tree('include', prefix.include)
            mkdirp(prefix.lib)
            install('lib*.a', prefix.lib)
            install('lib*.so', prefix.lib)
            install('lib*.dylib', prefix.lib)
