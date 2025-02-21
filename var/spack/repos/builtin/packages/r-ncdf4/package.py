# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNcdf4(RPackage):
    """Interface to Unidata netCDF (Version 4 or Earlier) Format Data Files.

    Provides a high-level R interface to data files written using Unidata's
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

    cran = "ncdf4"

    license("GPL-3.0-or-later")

    version("1.23", sha256="8b05fee9f79dc0605e487dd5d031d2c7dcaedec8f47904983b1c26739894da89")
    version("1.21", sha256="2f5ae7def382c595c66b6ed0ea0529f8337108eb73de39939f9762f3fb21b30d")
    version("1.19", sha256="cb8d139211fc7475c435ce9f6a43e47710603409dc523b053c8b7de9848dfb63")
    version("1.17", sha256="db95c4729d3187d1a56dfd019958216f442be6221bd15e23cd597e6129219af6")
    version("1.16.1", sha256="0dde2d6d1e8474f4abd15a61af8a2f7de564f13da00f1a01d7a479ab88587a20")
    version("1.16", sha256="edd5731a805bbece3a8f6132c87c356deafc272351e1dd07256ca00574949253")
    version("1.15", sha256="d58298f4317c6c80a041a70216126492fd09ba8ecde9da09d5145ae26f324d4d")

    depends_on("netcdf-c@4.1:")
