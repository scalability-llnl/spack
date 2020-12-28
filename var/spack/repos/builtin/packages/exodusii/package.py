# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


# TODO: Add support for a C++11 enabled installation that filters out the
# TODO: "C++11-Disabled" flag (but only if the spec compiler supports C++11).


class Exodusii(CMakePackage):
    """Exodus II is a C++/Fortran library developed to store and retrieve
       data for finite element analyses. It's used for preprocessing
       (problem definition), postprocessing (results visualization), and
       data transfer between codes.  An Exodus II data file is a random
       access, machine independent, binary file that is written and read
       via C, C++, or Fortran API routines.
    """

    homepage = "https://github.com/gsjaardema/seacas"
    git      = "https://github.com/gsjaardema/seacas.git"

    version('2016-08-09', commit='2ffeb1b')
    version('master', branch='master')

    variant('mpi', default=True, description='Enables MPI parallelism.')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('mpi', when='+mpi')

    # https://github.com/gsjaardema/seacas/blob/master/NetCDF-Mapping.md
    depends_on('netcdf-c@4.6.1:+mpi', when='+mpi')
    depends_on('netcdf-c@4.6.1:~mpi', when='~mpi')

    def cmake_args(self):
        spec = self.spec

        cc_path = spec['mpi'].mpicc if '+mpi' in spec else self.compiler.cc
        cxx_path = spec['mpi'].mpicxx if '+mpi' in spec else self.compiler.cxx

        options = [
            # General Flags #
            '-DSEACASProj_ENABLE_SEACASExodus=ON',
            '-DSEACASProj_ENABLE_TESTS=ON',
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DTPL_ENABLE_Netcdf:BOOL=ON',
            '-DHDF5_NO_SYSTEM_PATHS=ON',
            '-DSEACASProj_SKIP_FORTRANCINTERFACE_VERIFY_TEST:BOOL=ON',
            '-DSEACASProj_ENABLE_CXX11:BOOL=OFF',
            '-DSEACASProj_ENABLE_Zoltan:BOOL=OFF',
            '-DNetCDF_DIR:PATH={0}'.format(spec['netcdf-c'].prefix),

            # MPI Flags #
            '-DTPL_ENABLE_MPI={0}'.format('ON' if '+mpi' in spec else 'OFF'),
            '-DCMAKE_C_COMPILER={0}'.format(cc_path),
            '-DCMAKE_CXX_COMPILER={0}'.format(cxx_path),
        ]

        return options
