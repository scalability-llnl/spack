# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NetcdfCxx(AutotoolsPackage):
    """Deprecated C++ compatibility bindings for NetCDF.
    These do NOT read or write NetCDF-4 files, and are no longer
    maintained by Unidata.  Developers should migrate to current
    NetCDF C++ bindings, in Spack package netcdf-cxx4."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url = "https://downloads.unidata.ucar.edu/netcdf-cxx/4.2/netcdf-cxx-4.2.tar.gz"

    license("NetCDF")

    version("4.2", sha256="95ed6ab49a0ee001255eac4e44aacb5ca4ea96ba850c08337a3e4c9a0872ccd1")

    depends_on("cxx", type="build")  # generated

    depends_on("netcdf-c")

    variant("netcdf4", default=True, description="Compile with netCDF4 support")

    # https://github.com/Unidata/netcdf-cxx4/pull/112
    patch("macos.patch")

    @property
    def libs(self):
        shared = True
        return find_libraries("libnetcdf_c++", root=self.prefix, shared=shared, recursive=True)

    def configure_args(self):
        args = []
        if "+netcdf4" in self.spec:
            # There is no clear way to set this via configure, so set the flag
            # explicitly
            args.append("CPPFLAGS=-DUSE_NETCDF4")
        # Add these to LDFLAGS explicitly, so the linker doesn't accidentally
        # use system versions
        ldflags = [self.spec["netcdf-c"].libs.search_flags, self.spec["hdf5"].libs.search_flags]
        args.append("LDFLAGS=" + " ".join(ldflags))
        return args
