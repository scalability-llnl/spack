# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNcdf4(RPackage):
    """Provides a high-level R interface to data files written using Unidata's
    netCDF library (version 4 or earlier), which are binary data files that are
    portable across platforms and include metadata information in addition to
    the data sets. Using this package, netCDF files (either version 4 or
    "classic" version 3) can be opened and data sets read in easily. It is also
    easy to create new netCDF dimensions, variables, and files, in either
    version 3 or 4 format, and manipulate existing netCDF files. This package
    replaces the former ncdf package, which only worked with netcdf version 3
    files. For various reasons the names of the functions have had to be
    changed from the names in the ncdf package. The old ncdf package is still
    available at the URL given below, if you need to have backward
    compatibility. It should be possible to have both the ncdf and ncdf4
    packages installed simultaneously without a problem. However, the ncdf
    package does not provide an interface for netcdf version 4 files."""

    homepage = "http://cirrus.ucsd.edu/~pierce/ncdf"
    url      = "https://cloud.r-project.org/src/contrib/ncdf4_1.15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ncdf4"

    version('1.16.1', sha256='0dde2d6d1e8474f4abd15a61af8a2f7de564f13da00f1a01d7a479ab88587a20')
    version('1.16', sha256='edd5731a805bbece3a8f6132c87c356deafc272351e1dd07256ca00574949253')
    version('1.15', sha256='d58298f4317c6c80a041a70216126492fd09ba8ecde9da09d5145ae26f324d4d')

    depends_on('netcdf-c@4.1:')
