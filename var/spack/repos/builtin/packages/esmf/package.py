# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Esmf(MakefilePackage):
    """The Earth System Modeling Framework (ESMF) is high-performance, flexible
    software infrastructure for building and coupling weather, climate, and
    related Earth science applications. The ESMF defines an architecture for
    composing complex, coupled modeling systems and includes data structures
    and utilities for developing individual models."""

    homepage = "https://www.earthsystemcog.org/projects/esmf/"
    url      = "http://www.earthsystemmodeling.org/esmf_releases/public/ESMF_7_1_0r/esmf_7_1_0r_src.tar.gz"

    version('7.1.0r', sha256='ae9a5edb8d40ae97a35cbd4bd00b77061f995c77c43d36334dbb95c18b00a889')

    variant('mpi',     default=True,  description='Build with MPI support')
    variant('lapack',  default=True,  description='Build with LAPACK support')
    variant('netcdf',  default=True,  description='Build with NetCDF support')
    variant('pnetcdf', default=True,  description='Build with pNetCDF support')
    variant('xerces',  default=True,  description='Build with Xerces support')
    variant('pio',     default=True,  description='Enable ParallelIO support')
    variant('debug',   default=False, description='Make a debuggable version of the library')

    # Required dependencies
    depends_on('zlib')
    depends_on('libxml2')

    # Optional dependencies
    depends_on('mpi', when='+mpi')
    depends_on('lapack@3:', when='+lapack')
    depends_on('netcdf-c@3.6:', when='+netcdf')
    depends_on('netcdf-fortran@3.6:', when='+netcdf')
    depends_on('parallel-netcdf@1.2.0:', when='+pnetcdf')
    depends_on('xerces-c@3.1.0:', when='+xerces')

    # Testing dependencies
    depends_on('perl', type='test')

    # Make esmf build with newer intel versions
    patch('intel.patch', when='@:7.0.99 %intel@17:')
    # Make esmf build with newer gcc versions
    # https://sourceforge.net/p/esmf/esmf/ci/3706bf758012daebadef83d6575c477aeff9c89b/
    patch('gcc.patch', when='@:7.0.99 %gcc@6:')

    # Fix undefined reference errors with mvapich2
    # https://sourceforge.net/p/esmf/esmf/ci/34de0ccf556ba75d35c9687dae5d9f666a1b2a18/
    patch('mvapich2.patch', when='@:7.0.99')

    # Allow different directories for creation and
    # installation of dynamic libraries on OSX:
    patch('darwin_dylib_install_name.patch', when='platform=darwin @:7.0.99')

    # Missing include file for newer gcc compilers
    # https://trac.macports.org/ticket/57493
    patch('cstddef.patch', when='@7.1.0r %gcc@8:')

    # Make script from mvapich2.patch executable
    @when('@:7.0.99')
    @run_before('build')
    def chmod_scripts(self):
        chmod = which('chmod')
        chmod('+x', 'scripts/libs.mvapich2f90')

    def url_for_version(self, version):
        return "http://www.earthsystemmodeling.org/esmf_releases/public/ESMF_{0}/esmf_{0}_src.tar.gz".format(version.underscored)

    def edit(self, spec, prefix):
        # Installation instructions can be found at:
        # http://www.earthsystemmodeling.org/esmf_releases/last_built/ESMF_usrdoc/node9.html

        # Unset any environment variables that may influence the installation.
        for var in os.environ:
            if var.startswith('ESMF_'):
                os.environ.pop(var)

        ######################################
        # Build and Installation Directories #
        ######################################

        # The environment variable ESMF_DIR must be set to the full pathname
        # of the top level ESMF directory before building the framework.
        os.environ['ESMF_DIR'] = os.getcwd()

        # This variable specifies the prefix of the installation path used
        # with the install target.
        os.environ['ESMF_INSTALL_PREFIX'] = prefix

        # Installation subdirectories default to:
        # bin/binO/Linux.gfortran.64.default.default
        os.environ['ESMF_INSTALL_BINDIR'] = 'bin'
        os.environ['ESMF_INSTALL_LIBDIR'] = 'lib'
        os.environ['ESMF_INSTALL_MODDIR'] = 'include'

        # Allow compiler flags to carry through from compiler spec
        os.environ['ESMF_CXXCOMPILEOPTS'] = \
            ' '.join(spec.compiler_flags['cxxflags'])
        os.environ['ESMF_F90COMPILEOPTS'] = \
            ' '.join(spec.compiler_flags['fflags'])
        # ESMF will simply not build with Intel using backing GCC 8, in that
        # case you need to point to something older, below is commented but is
        # an example
        # os.environ['ESMF_CXXCOMPILEOPTS'] = \
        #     '-O2 -std=c++11 -gcc-name=/usr/bin/gcc'
        # os.environ['ESMF_F90COMPILEOPTS'] = \
        #     '-O2 -gcc-name=/usr/bin/gcc'

        ############
        # Compiler #
        ############

        # ESMF_COMPILER must be set to select which Fortran and
        # C++ compilers are being used to build the ESMF library.
        if self.compiler.name == 'gcc':
            os.environ['ESMF_COMPILER'] = 'gfortran'
        elif self.compiler.name == 'intel':
            os.environ['ESMF_COMPILER'] = 'intel'
        elif self.compiler.name == 'clang':
            os.environ['ESMF_COMPILER'] = 'gfortranclang'
        elif self.compiler.name == 'nag':
            os.environ['ESMF_COMPILER'] = 'nag'
        elif self.compiler.name == 'pgi':
            os.environ['ESMF_COMPILER'] = 'pgi'
        else:
            msg  = "The compiler you are building with, "
            msg += "'{0}', is not supported by ESMF."
            raise InstallError(msg.format(self.compiler.name))

        if '+mpi' in spec:
            os.environ['ESMF_CXX'] = spec['mpi'].mpicxx
            os.environ['ESMF_F90'] = spec['mpi'].mpifc
        else:
            os.environ['ESMF_CXX'] = os.environ['CXX']
            os.environ['ESMF_F90'] = os.environ['FC']

        # This environment variable controls the build option.
        if '+debug' in spec:
            # Build a debuggable version of the library.
            os.environ['ESMF_BOPT'] = 'g'
        else:
            # Build an optimized version of the library.
            os.environ['ESMF_BOPT'] = 'O'

        if self.spec.satisfies('%gcc@10:'):
            os.environ['ESMF_F90COMPILEOPTS'] = '-fallow-argument-mismatch'

        #######
        # MPI #
        #######

        # ESMF_COMM must be set to indicate which MPI implementation
        # is used to build the ESMF library.
        if '+mpi' in spec:
            if 'platform=cray' in self.spec:
                os.environ['ESMF_COMM'] = 'mpi'
            elif '^mvapich2' in spec:
                os.environ['ESMF_COMM'] = 'mvapich2'
            elif '^mpich' in spec:
                # esmf@7.0.1 does not include configs for mpich3,
                # so we start with the configs for mpich2:
                os.environ['ESMF_COMM'] = 'mpich2'
                # The mpich 3 series split apart the Fortran and C bindings,
                # so we link the Fortran libraries when building C programs:
                os.environ['ESMF_CXXLINKLIBS'] = '-lmpifort'
            elif '^openmpi' in spec:
                os.environ['ESMF_COMM'] = 'openmpi'
            elif '^intel-parallel-studio+mpi' in spec or '^intel-mpi' in spec:
                os.environ['ESMF_COMM'] = 'intelmpi'
        else:
            # Force use of the single-processor MPI-bypass library.
            os.environ['ESMF_COMM'] = 'mpiuni'

        ##########
        # LAPACK #
        ##########

        if '+lapack' in spec:
            # A system-dependent external LAPACK/BLAS installation is used
            # to satisfy the external dependencies of the LAPACK-dependent
            # ESMF code.
            os.environ['ESMF_LAPACK'] = 'system'

            # FIXME: determine whether or not we need to set this
            # Specifies the path where the LAPACK library is located.
            # os.environ['ESMF_LAPACK_LIBPATH'] = spec['lapack'].prefix.lib

            # Specifies the linker directive needed to link the LAPACK library
            # to the application.
            os.environ['ESMF_LAPACK_LIBS'] = spec['lapack'].libs.link_flags  # noqa
        else:
            # Disables LAPACK-dependent code.
            os.environ['ESMF_LAPACK'] = 'OFF'

        ##########
        # NetCDF #
        ##########

        if '+netcdf' in spec:
            # ESMF provides the ability to read Grid and Mesh data in
            # NetCDF format.
            if spec.satisfies('^netcdf-c@4.2:'):
                # ESMF_NETCDF_LIBS will be set to "-lnetcdff -lnetcdf".
                # This option is useful for systems which have the Fortran
                # and C bindings archived in seperate library files.
                os.environ['ESMF_NETCDF'] = 'split'
            else:
                # ESMF_NETCDF_LIBS will be set to "-lnetcdf".
                # This option is useful when the Fortran and C bindings
                # are archived together in the same library file.
                os.environ['ESMF_NETCDF'] = 'standard'

            # FIXME: determine whether or not we need to set these.
            # ESMF_NETCDF_INCLUDE
            # ESMF_NETCDF_LIBPATH

        ###################
        # Parallel-NetCDF #
        ###################

        if '+pnetcdf' in spec:
            # ESMF provides the ability to write Mesh weights
            # using Parallel-NetCDF.

            # When defined, enables the use of Parallel-NetCDF.
            # ESMF_PNETCDF_LIBS will be set to "-lpnetcdf".
            os.environ['ESMF_PNETCDF'] = 'standard'

            # FIXME: determine whether or not we need to set these.
            # ESMF_PNETCDF_INCLUDE
            # ESMF_PNETCDF_LIBPATH

        ##############
        # ParallelIO #
        ##############

        if '+pio' in spec and '+mpi' in spec:
            # ESMF provides the ability to read and write data in both binary
            # and NetCDF formats through ParallelIO (PIO), a third-party IO
            # software library that is integrated in the ESMF library.

            # PIO-dependent features will be enabled and will use the
            # PIO library that is included and built with ESMF.
            os.environ['ESMF_PIO'] = 'internal'
        else:
            # Disables PIO-dependent code.
            os.environ['ESMF_PIO'] = 'OFF'

        ##########
        # XERCES #
        ##########

        if '+xerces' in spec:
            # ESMF provides the ability to read Attribute data in
            # XML file format via the XERCES C++ library.

            # ESMF_XERCES_LIBS will be set to "-lxerces-c".
            os.environ['ESMF_XERCES'] = 'standard'

            # FIXME: determine if the following are needed
            # ESMF_XERCES_INCLUDE
            # ESMF_XERCES_LIBPATH

    def check(self):
        make('check', parallel=False)
