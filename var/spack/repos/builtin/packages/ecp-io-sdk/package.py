# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EcpIoSdk(BundlePackage):
    """ECP I/O Services SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"
    git      = "https://github.com/chuckatkins/ecp-data-viz-sdk.git"

    maintainers = ['chuckatkins']

    version('1.0', branch='master')

    variant('adios2', default=True, description="Enable ADIOS2")
    variant('darshan', default=True, description="Enable Darshan")
    variant('faodel', default=False, description="Enable FAODEL")
    variant('hdf5', default=True, description="Enable HDF5")
    variant('pnetcdf', default=True, description="Enable PNetCDF")
    variant('unifyfs', default=True, description="Enable UnifyFS")
    variant('veloc', default=True, description="Enable VeloC")

    depends_on('adios2+shared+mpi+fortran+python+zfp+sz+blosc+hdf5+sst+ssc+dataman', when='+adios2')
    depends_on('darshan-runtime+mpi', when='+darshan')
    depends_on('darshan-util', when='+darshan')
    depends_on('faodel+shared+mpi+hdf5 network=libfabric', when='+faodel')
    depends_on('hdf5+shared+mpi+fortran', when='+hdf5')
    depends_on('parallel-netcdf+shared+fortran', when='+pnetcdf')
    depends_on('unifyfs+fortran+hdf5', when='+unifyfs')
    depends_on('veloc', when='+veloc')
