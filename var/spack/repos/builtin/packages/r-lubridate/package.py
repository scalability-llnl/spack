# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLubridate(RPackage):
    """Make Dealing with Dates a Little Easier.

    Functions to work with date-times and timespans: fast and user friendly
    parsing of date-time data, extraction and updating of components of a
    date-time (years, months, days, hours, minutes, and seconds), algebraic
    manipulation on date-time and timespan objects. The 'lubridate' package has
    a consistent and memorable syntax that makes working with dates easy and
    fun."""

    cran = "lubridate"

    license("GPL-2.0-or-later")

    version("1.9.3", sha256="2b6e1406d231b0a14d60b99cc406d159fea5465a5694725ad25343f12cf37fff")
    version("1.9.2", sha256="8976431a4affe989261cbaa5e09cd44bb42a3b16eed59a42c1698da34c6544a7")
    version("1.9.0", sha256="b936041f8a71894ef930cfff61b45833e0dd148b5b16697f4f541d25b31a903a")
    version("1.8.0", sha256="87d66efdb1f3d680db381d7e40a202d35645865a0542e2f270ef008a19002ba5")
    version("1.7.9.2", sha256="ee6a2d68faca51646477acd1898ba774bf2b6fd474a0abf351b16aa5e7a3db79")
    version("1.7.4", sha256="510ca87bd91631c395655ee5029b291e948b33df09e56f6be5839f43e3104891")
    version("1.7.3", sha256="2cffbf54afce1d068e65241fb876a77b10ee907d5a19d2ffa84d5ba8a2c3f3df")
    version("1.7.1", sha256="898c3f482ab8f5e5b415eecd13d1238769c88faed19b63fcb074ffe5ff57fb5f")
    version("1.5.6", sha256="9b1627ba3212e132ce2b9a29d7513e250cc682ab9b4069f6788a22e84bf8d2c4")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@1.7.9.2:")
    depends_on("r-generics", type=("build", "run"), when="@1.7.9.2:")

    depends_on("r-rcpp@0.12.13:", type=("build", "run"), when="@:1.7")
    depends_on("r-timechange@0.1.1:", type=("build", "run"), when="@1.9.0:")
    depends_on("r-stringr", type=("build", "run"), when="@:1.7.4")
    depends_on("r-cpp11", type=("build", "run"), when="@:1.8.0")
    depends_on("r-cpp11@0.2.7:", type=("build", "run"), when="@1.8.0")
