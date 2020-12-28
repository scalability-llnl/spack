# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tioga(CMakePackage):
    """Topology Independent Overset Grid Assembly (TIOGA)"""

    homepage = "https://github.com/jsitaraman/tioga"
    git      = "https://github.com/jsitaraman/tioga.git"

    version('master', branch='master')

    variant('shared', default=True,
            description="Enable building shared libraries")
    variant('pic', default=True,
            description="Position independent code")

    depends_on('mpi')

    # Tioga has the fortran module file problem with parallel builds
    parallel = False

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=%s' % (
                'ON' if '+pic' in spec else 'OFF'),
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DMPI_CXX_COMPILER:PATH=%s' % spec['mpi'].mpicxx,
            '-DMPI_C_COMPILER:PATH=%s' % spec['mpi'].mpicc,
            '-DMPI_Fortran_COMPILER:PATH=%s' % spec['mpi'].mpifc
        ]

        if 'darwin' in spec.architecture:
            options.append('-DCMAKE_MACOSX_RPATH:BOOL=ON')

        return options
