# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class W3emc(CMakePackage):
    """This library contains Fortran 90 decoder/encoder routines for GRIB
    edition 1 with EMC changes.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-w3emc/"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-w3emc/archive/refs/tags/v2.9.0.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-w3emc"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("2.12.0", sha256="77c0732541ade1deb381f5a208547ccc36e65efa91c8f7021b299b20a6ae0d27")
    version("2.11.0", sha256="53a03d03421c5da699b026ca220512ed494a531b83284693f66d2579d570c43b")
    version("2.10.0", sha256="366b55a0425fc3e729ecb9f3b236250349399fe4c8e19f325500463043fd2f18")
    version("2.9.3", sha256="9ca1b08dd13dfbad4a955257ae0cf38d2e300ccd8d983606212bc982370a29bc")
    version("2.9.2", sha256="eace811a1365f69b85fdf2bcd93a9d963ba72de5a7111e6fa7c0e6578b69bfbc")
    version("2.9.1", sha256="d3e705615bdd0b76a40751337d943d5a1ea415636f4e5368aed058f074b85df4")
    version("2.9.0", sha256="994f59635ab91e34e96cab5fbaf8de54389d09461c7bac33b3104a1187e6c98a")
    version("2.7.3", sha256="eace811a1365f69b85fdf2bcd93a9d963ba72de5a7111e6fa7c0e6578b69bfbc")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("pic", default=True, description="Build with position-independent-code")
    variant("bufr", default=False, description="Build with BUFR routines", when="@2.10:")
    variant(
        "precision",
        default=("4", "d"),
        values=("4", "d", "8"),
        multi=True,
        description="Set precision (_4/_d/_8 library versions)",
        when="@2.10:",
    )
    variant("shared", default=False, description="Build shared library", when="@2.10: +pic")
    variant(
        "extradeps",
        default=False,
        description="Build w3emc with subprograms which call unknown dependencies",
        when="@2.10:2.11",
    )
    variant(
        "build_deprecated",
        default=False,
        description="Build deprecated subroutines",
        when="@2.12:",
    )

    conflicts("+shared +extradeps", msg="Shared library cannot be built with unknown dependencies")

    depends_on("bufr", when="@2.10: +bufr")
    depends_on("bacio", when="@2.9.2:")

    # w3emc 2.7.3 contains gblevents which has these dependencies
    depends_on("nemsio", when="@2.7.3")
    depends_on("sigio", when="@2.7.3")
    depends_on("netcdf-fortran", when="@2.7.3")

    def setup_run_environment(self, env):
        if self.spec.satisfies("@:2.9"):
            suffixes = ("4", "d", "8")
            shared = False
        else:
            suffixes = self.spec.variants["precision"].value
            shared = self.spec.satisfies("+shared")

        for suffix in suffixes:
            lib = find_libraries(
                "libw3emc_" + suffix, root=self.prefix, shared=shared, recursive=True
            )
            env.set("W3EMC_LIB" + suffix, lib[0])
            env.set("W3EMC_INC" + suffix, join_path(self.prefix, "include_" + suffix))

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_WITH_BUFR", "bufr"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define("BUILD_4", self.spec.satisfies("precision=4")),
            self.define("BUILD_D", self.spec.satisfies("precision=d")),
            self.define("BUILD_8", self.spec.satisfies("precision=8")),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_WITH_EXTRA_DEPS", "extradeps"),
            self.define_from_variant("BUILD_DEPRECATED", "build_deprecated"),
        ]

        return args

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
