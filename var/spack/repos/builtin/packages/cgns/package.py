# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from spack import *


class Cgns(CMakePackage):
    """The CFD General Notation System (CGNS) provides a general, portable,
    and extensible standard for the storage and retrieval of computational
    fluid dynamics (CFD) analysis data."""

    homepage = "http://cgns.github.io/"
    url      = "https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz"
    git      = "https://github.com/CGNS/CGNS"

    parallel = False

    version('develop', branch='develop')
    version('master',  branch='master')
    version('4.1.1',   sha256='055d345c3569df3ae832fb2611cd7e0bc61d56da41b2be1533407e949581e226')
    version('4.1.0',   sha256='4674de1fac3c47998248725fd670377be497f568312c5903d1bb8090a3cf4da0')
    version('4.0.0',   sha256='748585a8e52dff4d250d6b603e6b847d05498e4566aba2dc3d7a7d85c4d55849')
    version('3.4.1',   sha256='d32595e7737b9332243bd3de1eb8c018a272f620f09b289dea8292eba1365994')
    version('3.4.0',   sha256='6372196caf25b27d38cf6f056258cb0bdd45757f49d9c59372b6dbbddb1e05da')
    version('3.3.1',   sha256='81093693b2e21a99c5640b82b267a495625b663d7b8125d5f1e9e7aaa1f8d469')
    version('3.3.0',   sha256='8422c67994f8dc6a2f201523a14f6c7d7e16313bdd404c460c16079dbeafc662')

    variant('hdf5',       default=True,  description='Enable HDF5 interface')
    variant('fortran',    default=False, description='Enable Fortran interface')
    variant('base_scope', default=False, description='Enable base scope')
    variant('scoping',    default=True,  description='Enable scoping')
    variant('mpi',        default=True,  description='Enable parallel cgns')
    variant('int64',      default=False, description='Build with 64-bit integers')
    variant('shared',     default=True,  description='Enable shared library')
    variant('static',     default=False, description='Build static libraries')
    variant('testing',    default=False, description='Build CGNS testing')
    variant('legacy',     default=False, description='Enable legacy options')
    variant('parallel',   default=False, description='Enable parallel features')
    variant('mem_debug',  default=False, description='Enable memory debugging option')

    depends_on('hdf5~mpi', when='+hdf5~mpi')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DCGNS_ENABLE_FORTRAN:BOOL=%s' % (
                'ON' if '+fortran' in spec else 'OFF'),
            '-DCGNS_ENABLE_SCOPING:BOOL=%s' % (
                'ON' if '+scoping' in spec else 'OFF'),
            '-DCGNS_ENABLE_PARALLEL:BOOL=%s' % (
                'ON' if '+mpi' in spec else 'OFF'),
            '-DCGNS_ENABLE_TESTS:BOOL=OFF',
            '-DCGNS_BUILD_TESTING:BOOL=%s' % (
                'ON' if '+testing' in spec else 'OFF'),
            '-DCGNS_BUILD_CGNSTOOLS:BOOL=OFF',
            '-DCGNS_BUILD_SHARED:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DCGNS_BUILD_STATIC:BOOL=%s' % (
                'ON' if '+static' in spec else 'OFF'),
            '-DCGNS_ENABLE_BASE_SCOPE:BOOL=%s' % (
                'ON' if '+base_scope' in spec else 'OFF'),
            '-DCGNS_ENABLE_LEGACY:BOOL=%s' % (
                'ON' if '+legacy' in spec else 'OFF'),
            '-DCGNS_ENABLE_PARALLEL:BOOL=%s' % (
                'ON' if '+parallel' in spec else 'OFF'),
            '-DCGNS_ENABLE_MEM_DEBUG:BOOL=%s' % (
                'ON' if '+mem_debug' in spec else 'OFF')
        ])

        if '+mpi' in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
            ])

        options.append(
            '-DCGNS_ENABLE_64BIT:BOOL={0}'.format(
                'ON' if '+int64' in spec else 'OFF'))

        if '+hdf5' in spec:
            options.extend([
                '-DCGNS_ENABLE_HDF5:BOOL=ON',
                '-DHDF5_NEED_ZLIB:BOOL=ON',
                '-DHDF5_INCLUDE_DIR:PATH=%s' % spec['hdf5'].prefix.include,
                '-DHDF5_LIBRARY_DIR:PATH=%s' % spec['hdf5'].prefix.lib
            ])
            if '+mpi' in spec:
                options.extend([
                    '-DHDF5_NEED_MPI:BOOL=ON',
                    '-DHDF5_ENABLE_PARALLEL:BOOL=ON'
                ])
        else:
            options.extend(['-DCGNS_ENABLE_HDF5=OFF'])

        if self.version <= Version('3.3.1'):
            if sys.platform == 'darwin':
                options.extend([
                    '-DCMAKE_MACOSX_RPATH:BOOL=ON'
                ])

        return options
