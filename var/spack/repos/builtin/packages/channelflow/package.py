# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Channelflow(CMakePackage):
    """Channelflow is a software system for numerical analysis of the
    incompressible fluid flow in channel geometries, written in C++.
    """

    homepage = 'https://github.com/epfl-ecps/channelflow'
    git      = 'https://github.com/epfl-ecps/channelflow.git'

    version('master', branch='master')

    variant('shared', default=True, description='Build shared libs')
    variant('mpi', default=True, description='Enable MPI parallelism')
    variant('hdf5', default=True, description='Enable support for HDF5 I/O')
    variant(
        'netcdf', default='serial', values=('none', 'serial', 'parallel'),
        multi=False, description='Level of support for NetCDF I/O'
    )
    variant('python', default=False, description='Build python bindings')

    depends_on('eigen')
    depends_on('fftw')

    # MPI related constraints
    depends_on('mpi', when='+mpi')
    depends_on('fftw+mpi', when='+mpi')

    # Support for different I/O formats
    depends_on('hdf5+cxx', when='+hdf5')
    depends_on('netcdf-c', when='netcdf=serial')
    depends_on('netcdf-c+mpi', when='netcdf=parallel')

    # Python bindings
    depends_on('boost+python', when='+python')

    conflicts('~mpi', when='netcdf=parallel', msg='Parallel NetCDF requires MPI')
    conflicts(
        '+mpi', when='+python',
        msg='Building python bindings is possible only for the serial code'
    )
    conflicts('~mpi', when='^mpi',
              msg='There should be no MPI in the DAG when ~mpi is active')

    def cmake_args(self):
        spec = self.spec

        on_or_off = lambda predicate: 'ON' if predicate else 'OFF'

        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                on_or_off('+shared' in spec)
            ),
            '-DUSE_MPI:BOOL={0}'.format(on_or_off('+mpi' in spec)),
            '-DWITH_HDF5CXX:BOOL={0}'.format(on_or_off('+hdf5' in spec)),
            '-DWITH_PYTHON:BOOL={0}'.format(on_or_off('+python' in spec))
        ]

        netcdf_str = {
            'none': 'OFF',
            'serial': 'Serial',
            'parallel': 'Parallel'
        }

        args.append('-DWITH_NETCDF:STRING={0}'.format(
            netcdf_str[spec.variants['netcdf'].value]
        ))

        # Set an MPI compiler for parallel builds
        if '+mpi' in spec:
            args.append(
                '-DCMAKE_CXX_COMPILER:PATH={0}'.format(spec['mpi'].mpicxx)
            )

        return args
