# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

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
    url      = "https://github.com/gsjaardema/seacas/archive/refs/tags/v2021-04-05.zip"

    version('2021-04-05', sha256='f40d318674753287b8b28d2b4e5cca872cd772d4c7383af4a8f3eeb48fcc7ec0')
    version('2021-04-02', sha256='811037a68eaff0daf9f34bd31b2ab1c9b8f028dfcb998ab01fbcb80d9458257c')
    version('2021-01-20', sha256='6ff7c3f0651138f2e2305b5270108ca45f96346a739b35a126a0a260c91cbe64')
    version('2021-01-06', sha256='69cafef17d8e624c2d9871f3a281ff3690116a6f82162fe5c1507bb4ecd6a32a')
    version('2020-08-13', sha256='5b128a8ad9b0a69cff4fe937828d6d1702f1fe8aa80d4751e6522939afe62957')
    version('2020-05-12', sha256='0402facf6cf23d903d878fb924b5d57e9f279dead5b92cf986953a6b91a6e81f')
    version('2020-03-16', sha256='ed1d42c8c657931ecd45367a465cf9c00255772d9cd0811fc9baacdb67fc71fa')
    version('2020-01-16', sha256='db69dca25595e88a40c00db0ccf2afed1ecd6008ba30bb478a4e1c5dd61998b8')
    version('2019-12-18', sha256='88a71de836aa26fd63756cf3ffbf3978612edc5b6c61fa8de32fe9d638007774')
    version('2019-10-14', sha256='f143d90e8a7516d25979d1416e580dea638332db723f26ae94a712dfe4052e8f')
    version('2016-08-09', commit='2ffeb1b')
    version('master', branch='master')

    variant('mpi', default=True, description='Enables MPI parallelism.')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('mpi', when='+mpi')

    # https://github.com/gsjaardema/seacas/blob/master/NetCDF-Mapping.md
    depends_on('netcdf-c@4.6.1:+mpi', when='+mpi')
    depends_on('netcdf-c@4.6.1:~mpi', when='~mpi')

    depends_on('python@2.7:')

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
        # Python #
        # Handle v2016 separately because of older tribits
        if spec.satisfies('@:2016-08-09'):
            options.append('-DPYTHON_EXECUTABLE={0}'.format(
                join_path(self.spec['python'].prefix.bin, 'python')))
        else:
            options.append('-DPython_ROOT={0}'.format(spec['python'].prefix))

        return options
