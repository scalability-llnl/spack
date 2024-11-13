# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cdi(AutotoolsPackage):
    """
    CDI is a C and Fortran Interface to access Climate and NWP model Data.
    Supported data formats are GRIB, netCDF, SERVICE, EXTRA and IEG.
    """

    homepage = "https://code.mpimet.mpg.de/projects/cdi"
    url = "https://code.mpimet.mpg.de/attachments/download/29309/cdi-2.4.0.tar.gz"

    version("2.4.0", sha256="91fca015b04c6841b9eab8b49e7726d35e35b9ec4350922072ec6e9d5eb174ef")

    variant(
        "netcdf", default=True, description="This is needed to read/write NetCDF files with CDI"
    )

    depends_on("netcdf-c", when="+netcdf")

    def configure_args(self):
        args = []
        if "+netcdf" in self.spec:
            args.append("--with-netcdf=" + self.spec["netcdf-c"].prefix)
        return args
