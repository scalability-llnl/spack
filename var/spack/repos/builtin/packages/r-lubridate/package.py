# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLubridate(RPackage):
    """Functions to work with date-times and timespans: fast and user friendly
    parsing of date-time data, extraction and updating of components of a
    date-time (years, months, days, hours, minutes, and seconds), algebraic
    manipulation on date-time and timespan objects. The 'lubridate' package has
    a consistent and memorable syntax that makes working with dates easy and
    fun."""

    homepage = "https://cloud.r-project.org/package=lubridate"
    url      = "https://cloud.r-project.org/src/contrib/lubridate_1.7.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lubridate"

    version('1.7.4', sha256='510ca87bd91631c395655ee5029b291e948b33df09e56f6be5839f43e3104891')
    version('1.7.3', sha256='2cffbf54afce1d068e65241fb876a77b10ee907d5a19d2ffa84d5ba8a2c3f3df')
    version('1.7.1', sha256='898c3f482ab8f5e5b415eecd13d1238769c88faed19b63fcb074ffe5ff57fb5f')
    version('1.5.6', sha256='9b1627ba3212e132ce2b9a29d7513e250cc682ab9b4069f6788a22e84bf8d2c4')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.13:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
