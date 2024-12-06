# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libemos(CMakePackage):
    """The Interpolation library (EMOSLIB) includes Interpolation software and
    BUFR & CREX encoding/decoding routines."""

    homepage = "https://software.ecmwf.int/wiki/display/EMOS/Emoslib"
    url = (
        "https://software.ecmwf.int/wiki/download/attachments/3473472/libemos-4.4.2-Source.tar.gz"
    )
    list_url = "https://software.ecmwf.int/wiki/display/EMOS/Releases"

    license("Apache-2.0")

    version("4.5.1", sha256="c982d9fd7dcd15c3a4d1e1115b90430928b660e17f73f7d4e360dd9f87f68c46")
    version("4.5.0", sha256="debe474603224c318f8ed4a1c209a4d1416807c594c3faa196059b2228824393")
    version("4.4.9", sha256="61af7dfcd37875b4f834e2e4371922ec529a8c03879c52e8fb911b35e4c0d413")
    version("4.4.7", sha256="669fb070c1ce655812882140a92b100233f065829868d9374bad2fcbb6b356e5")
    version("4.4.2", sha256="e2d20ad71e3beb398916f98a35a3c56ee0141d5bc9b3adff15095ff3b6dccea8")

    variant(
        "grib",
        default="eccodes",
        values=("eccodes", "grib-api"),
        description="Specify GRIB backend",
    )
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo", "Production"),
    )

    depends_on("eccodes", when="grib=eccodes")
    depends_on("grib-api", when="grib=grib-api")
    depends_on("fftw precision=float,double")
    depends_on("cmake@2.8.11:", type="build")
    depends_on("pkgconfig", type="build")

    conflicts("grib=eccodes", when="@:4.4.1", msg="Eccodes is supported starting version 4.4.2")

    def cmake_args(self):
        args = []

        if self.spec.variants["grib"].value == "eccodes":
            args.append("-DENABLE_ECCODES=ON")
        else:
            if self.spec.satisfies("@4.4.2:"):
                args.append("-DENABLE_ECCODES=OFF")

        # To support long pathnames that spack generates
        args.append("-DCMAKE_Fortran_FLAGS=-ffree-line-length-none")

        return args
