# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os, shutil, distutils.core

class Netcdf(BundlePackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is a "meta" package that
    includes the C, C++, and Fortran distributions."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"

    maintainers = ['vanderwb']

    version('4.9.2')
    version('4.9.1')
    version('4.9.0')
    version('4.8.1')

    # Inherit relevant variants from netcdf-c package
    variant('mpi', default=False,
            description='Enable parallel I/O for netcdf-4')
    variant('parallel-netcdf', default=False,
            description='Enable parallel I/O for classic files')
    variant('hdf4', default=False, description='Enable HDF4 support')
    variant('dap', default=False, description='Enable DAP support')

    depends_on('netcdf-c +mpi', when='+mpi')
    depends_on('netcdf-c ~mpi', when='~mpi')
    depends_on('netcdf-c +dap', when='+dap')
    depends_on('netcdf-c ~dap', when='~dap')
    depends_on('netcdf-c +hdf4', when='+hdf4')
    depends_on('netcdf-c ~hdf4', when='~hdf4')
    depends_on('netcdf-c +parallel-netcdf', when='+parallel-netcdf')
    depends_on('netcdf-c ~parallel-netcdf', when='~parallel-netcdf')
    depends_on('netcdf-fortran')
    depends_on('netcdf-cxx4')

    depends_on('netcdf-c@4.9.2', when='@4.9.2')
    depends_on('netcdf-c@4.9.1', when='@4.9.1')
    depends_on('netcdf-c@4.9.0', when='@4.9.0')
    depends_on('netcdf-c@4.8.1', when='@4.8.1')
    depends_on('netcdf-fortran@4.6.1', when='@4.9.2:')
    depends_on('netcdf-fortran@4.6.0', when='@4.9.0:4.9.1')
    depends_on('netcdf-fortran@4.5.3', when='@4.8.1')
    depends_on('netcdf-cxx4@4.3.1', when='@4.8.1:')

    def install(self, spec, prefix):
        for dep in ['netcdf-c', 'netcdf-fortran', 'netcdf-cxx4']:
            dep_prefix = self.spec[dep].prefix

            for subdir in os.listdir(dep_prefix):
                # Avoid copying Spack metadata - will corrupt database
                if not subdir.startswith('.'):
                    dep_sub = join_path(dep_prefix, subdir)
                    my_sub  = join_path(prefix, subdir)

                    try:
                        distutils.dir_util.copy_tree(dep_sub, my_sub)
                    except:
                        shutil.copytree(dep_sub, my_sub, dirs_exist_ok = True)

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.
        """

        env.set("NETCDF", self.prefix)
