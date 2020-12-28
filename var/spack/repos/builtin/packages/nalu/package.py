# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Nalu(CMakePackage):
    """Nalu: a generalized unstructured massively parallel low Mach flow code
       designed to support a variety of energy applications of interest
       built on the Sierra Toolkit and Trilinos solver Tpetra/Epetra stack
    """

    homepage = "https://github.com/NaluCFD/Nalu"
    git      = "https://github.com/NaluCFD/Nalu.git"

    version('master', branch='master')

    # Options
    variant('shared', default=(sys.platform != 'darwin'),
            description='Build dependencies as shared libraries')
    variant('pic', default=True,
            description='Position independent code')
    # Third party libraries
    variant('tioga', default=False,
            description='Compile with Tioga support')

    # Required dependencies
    depends_on('mpi')
    depends_on('yaml-cpp@0.5.3:', when='+shared')
    depends_on('yaml-cpp~shared@0.5.3:', when='~shared')
    # Cannot build Trilinos as a shared library with STK on Darwin
    # which is why we have a 'shared' variant for Nalu
    # https://github.com/trilinos/Trilinos/issues/2994
    depends_on('trilinos+exodus+tpetra+muelu+belos+ifpack2+amesos2+zoltan+stk+boost~superlu-dist+superlu+hdf5+zlib+pnetcdf+shards~hypre@master,develop', when='+shared')
    depends_on('trilinos~shared+exodus+tpetra+muelu+belos+ifpack2+amesos2+zoltan+stk+boost~superlu-dist+superlu+hdf5+zlib+pnetcdf+shards~hypre@master,develop', when='~shared')
    # Optional dependencies
    depends_on('tioga', when='+tioga+shared')
    depends_on('tioga~shared', when='+tioga~shared')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DTrilinos_DIR:PATH=%s' % spec['trilinos'].prefix,
            '-DYAML_DIR:PATH=%s' % spec['yaml-cpp'].prefix,
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DMPI_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DMPI_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DMPI_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=%s' % (
                'ON' if '+pic' in spec else 'OFF'),
        ])

        if '+tioga' in spec:
            options.extend([
                '-DENABLE_TIOGA:BOOL=ON',
                '-DTIOGA_DIR:PATH=%s' % spec['tioga'].prefix
            ])
        else:
            options.append('-DENABLE_TIOGA:BOOL=OFF')

        if 'darwin' in spec.architecture:
            options.append('-DCMAKE_MACOSX_RPATH:BOOL=ON')

        return options
