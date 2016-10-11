##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing,
       machine-independent data formats that support the creation, access,
       and sharing of array-oriented scientific data.

    """

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.4.1', '7843e35b661c99e1d49e60791d5072d8')
    version('4.4.0', 'cffda0cbd97fdb3a06e9274f7aef438e')
    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('mpi',  default=True,  description='Enables MPI parallelism')
    variant('hdf4', default=False, description='Enable HDF4 support')
    # These variants control the number of dimensions (i.e. coordinates and
    # attributes) and variables (e.g. time, entity ID, number of coordinates)
    # that can be used in any particular NetCDF file.
    variant('maxdims', default=1024,
            description='Defines the maximum dimensions of NetCDF files.')
    variant('maxvars', default=8192,
            description='Defines the maximum variables of NetCDF files.')

    depends_on("m4", type='build')
    depends_on("hdf", when='+hdf4')

    # Required for DAP support
    depends_on("curl@7.18.0:")

    # Required for NetCDF-4 support
    depends_on("zlib@1.2.5:")
    depends_on('hdf5')

    # NetCDF 4.4.0 and prior have compatibility issues with HDF5 1.10 and later
    # https://github.com/Unidata/netcdf-c/issues/250
    depends_on('hdf5@:1.8', when='@:4.4.0')

    def patch(self):
        try:
            max_dims = int(self.spec.variants['maxdims'].value)
            max_vars = int(self.spec.variants['maxvars'].value)
        except (ValueError, TypeError):
            raise TypeError('NetCDF variant values max[dims|vars] must be '
                            'integer values.')

        ff = FileFilter(join_path('include', 'netcdf.h'))
        ff.filter(r'^(#define\s+NC_MAX_DIMS\s+)\d+(.*)$',
                  r'\1{0}\2'.format(max_dims))
        ff.filter(r'^(#define\s+NC_MAX_VARS\s+)\d+(.*)$',
                  r'\1{0}\2'.format(max_vars))

    def install(self, spec, prefix):
        # Workaround until variant forwarding works properly
        if '+mpi' in spec and spec.satisfies('^hdf5~mpi'):
            raise RuntimeError('Invalid spec. Package netcdf requires '
                               'hdf5+mpi, but spec asked for hdf5~mpi.')

        # Environment variables
        CPPFLAGS = []
        LDFLAGS  = []
        LIBS     = []

        config_args = [
            "--prefix=%s" % prefix,
            "--enable-fsync",
            "--enable-v2",
            "--enable-utilities",
            "--enable-shared",
            "--enable-static",
            "--enable-largefile",
            # necessary for HDF5 support
            "--enable-netcdf-4",
            "--enable-dynamic-loading",
            # necessary for DAP support
            "--enable-dap"
        ]

        # Make sure Netcdf links against Spack's curl, otherwise
        # otherwise it may pick up system's curl, which can give link
        # errors, e.g.:
        # undefined reference to `SSL_CTX_use_certificate_chain_file`
        LIBS.append("-lcurl")
        CPPFLAGS.append("-I%s" % spec['curl'].prefix.include)
        LDFLAGS.append("-L%s" % spec['curl'].prefix.lib)

        if '+mpi' in spec:
            config_args.append('--enable-parallel4')

        CPPFLAGS.append("-I%s/include" % spec['hdf5'].prefix)
        LDFLAGS.append("-L%s/lib"     % spec['hdf5'].prefix)

        # HDF4 support
        # As of NetCDF 4.1.3, "--with-hdf4=..." is no longer a valid option
        # You must use the environment variables CPPFLAGS and LDFLAGS
        if '+hdf4' in spec:
            config_args.append("--enable-hdf4")
            CPPFLAGS.append("-I%s/include" % spec['hdf'].prefix)
            LDFLAGS.append("-L%s/lib"     % spec['hdf'].prefix)
            LIBS.append("-l%s"         % "jpeg")

        if '+szip' in spec:
            CPPFLAGS.append("-I%s/include" % spec['szip'].prefix)
            LDFLAGS.append("-L%s/lib"     % spec['szip'].prefix)
            LIBS.append("-l%s"         % "sz")

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # Use the netcdf-fortran package to install Fortran support.

        config_args.append('CPPFLAGS=%s' % ' '.join(CPPFLAGS))
        config_args.append('LDFLAGS=%s'  % ' '.join(LDFLAGS))
        config_args.append('LIBS=%s'     % ' '.join(LIBS))

        configure(*config_args)
        make()

        if self.run_tests:
            make("check")

        make("install")
