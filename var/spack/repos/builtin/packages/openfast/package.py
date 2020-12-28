# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openfast(CMakePackage):
    """Wind turbine simulation package from NREL"""

    homepage = "http://openfast.readthedocs.io/en/latest/"
    git      = "https://github.com/OpenFAST/openfast.git"

    maintainers = ['jrood-nrel']

    version('develop', branch='dev')
    version('master', branch='master')

    variant('shared', default=True,
            description="Build shared libraries")
    variant('double-precision', default=True,
            description="Treat REAL as double precision")
    variant('dll-interface', default=True,
            description="Enable dynamic library loading interface")
    variant('cxx', default=False,
            description="Enable C++ bindings")
    variant('pic', default=True,
            description="Position independent code")

    # Dependencies for OpenFAST Fortran
    depends_on('blas')
    depends_on('lapack')

    # Additional dependencies when compiling C++ library
    depends_on('mpi', when='+cxx')
    depends_on('yaml-cpp', when='+cxx')
    depends_on('hdf5+mpi+cxx+hl', when='+cxx')
    depends_on('zlib', when='+cxx')
    depends_on('libxml2', when='+cxx')

    def cmake_args(self):
        spec = self.spec

        options = []

        options.extend([
            '-DBUILD_DOCUMENTATION:BOOL=OFF',
            '-DBUILD_TESTING:BOOL=OFF',
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DDOUBLE_PRECISION:BOOL=%s' % (
                'ON' if '+double-precision' in spec else 'OFF'),
            '-DUSE_DLL_INTERFACE:BOOL=%s' % (
                'ON' if '+dll-interface' in spec else 'OFF'),
            '-DBUILD_OPENFAST_CPP_API:BOOL=%s' % (
                'ON' if '+cxx' in spec else 'OFF'),
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=%s' % (
                'ON' if '+pic' in spec else 'OFF'),
        ])

        # Make sure we use Spack's blas/lapack:
        blas_libs = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            '-DBLAS_LIBRARIES=%s' % blas_libs.joined(';'),
            '-DLAPACK_LIBRARIES=%s' % blas_libs.joined(';')
        ])

        if '+cxx' in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                '-DMPI_CXX_COMPILER:PATH=%s' % spec['mpi'].mpicxx,
                '-DMPI_C_COMPILER:PATH=%s' % spec['mpi'].mpicc,
                '-DMPI_Fortran_COMPILER:PATH=%s' % spec['mpi'].mpifc,
                '-DHDF5_ROOT:PATH=%s' % spec['hdf5'].prefix,
                '-DYAML_ROOT:PATH=%s' % spec['yaml-cpp'].prefix,
            ])

            if '~shared' in spec:
                options.extend([
                    '-DHDF5_USE_STATIC_LIBRARIES=ON',
                ])

        if 'darwin' in spec.architecture:
            options.append('-DCMAKE_MACOSX_RPATH:BOOL=ON')

        return options
