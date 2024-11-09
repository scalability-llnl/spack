# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GribUtil(CMakePackage):
    """This is a collection of NCEP GRIB related utilities.

    This is related to NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util/archive/refs/tags/v1.2.3.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-grib_util"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("1.5.0", tag="v1.5.0", commit="b84e877a62efe6695546a4b7a02e7adb6e1ece25")
    version("1.4.0", tag="v1.4.0", commit="eeacc9ec93dfe6379f576191883c84a4a1202cc8")
    version("1.3.0", commit="9d3c68a")
    version("1.2.4", sha256="f021d6df3186890b0b1781616dabf953581d71db63e7c2913360336985ccaec7")
    version("1.2.3", sha256="b17b08e12360bb8ad01298e615f1b4198e304b0443b6db35fe990a817e648ad5")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("openmp", default=False, description="Use OpenMP multithreading")
    variant("tests", default=False, description="Enable this variant when installing with --test")

    depends_on("jasper")
    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("w3emc +extradeps", when="@1.2.4:")
    requires("^w3emc precision=4,d", when="^w3emc@2.10:")
    depends_on("w3nco", when="@:1.2.3")
    depends_on("g2")
    depends_on("g2@3.4.9:", when="@1.4")
    depends_on("g2@3.5:", when="@1.5:")
    depends_on("g2c@1.8: +utils", when="+tests")
    depends_on("bacio")
    depends_on("ip")
    requires("^ip precision=d", when="^ip@4.1:")
    depends_on("ip@:3.3.3", when="@:1.2")
    depends_on("sp", when="^ip@:4")
    requires("^sp precision=d", when="^ip@:4 ^sp@2.4:")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP", "openmp"),
            self.define("BUILD_TESTING", self.run_tests),
            self.define("G2C_COMPARE", self.run_tests),
        ]
        return args

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
