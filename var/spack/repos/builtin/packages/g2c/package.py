# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class G2c(CMakePackage):
    """This library contains C decoder/encoder routines for GRIB edition 2.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-g2c"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-g2c/archive/refs/tags/v1.6.4.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-g2c"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("1.9.0", sha256="5554276e18bdcddf387a08c2dd23f9da310c6598905df6a2a244516c22ded9aa")
    version("1.8.0", sha256="4ce9f5a7cb0950699fe08ebc5a463ab4d09ef550c050391a319308a2494f971f")
    version("1.7.0", sha256="73afba9da382fed73ed8692d77fa037bb313280879cd4012a5e5697dccf55175")
    version("1.6.4", sha256="5129a772572a358296b05fbe846bd390c6a501254588c6a223623649aefacb9d")
    version("1.6.2", sha256="b5384b48e108293d7f764cdad458ac8ce436f26be330b02c69c2a75bb7eb9a2c")

    depends_on("c", type="build")

    variant("aec", default=True, description="Use AEC library")
    variant("png", default=True, description="Use PNG library")
    variant("jasper", default=True, description="Use Jasper library")
    variant("openjpeg", default=False, description="Use OpenJPEG library")
    variant("pic", default=True, description="Build with position-independent-code")
    variant(
        "libs",
        default=("shared", "static"),
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
        when="@1.7:",
    )
    variant(
        "pthreads",
        default=False,
        description="Turn on thread-safety with pthreads",
        when="@develop",
    )
    variant(
        "utils",
        default=True,
        description="Build and install some utility programs",
        when="@develop",
    )
    variant(
        "build_v2_api",
        default=False,
        description="Build new g2c API, experimental until 2.0.0 release",
        when="@develop",
    )

    depends_on("libaec", when="+aec")
    depends_on("libpng", when="+png")
    depends_on("jasper", when="+jasper")
    depends_on("openjpeg", when="+openjpeg")
    depends_on("libxml2@2.9:", when="+build_v2_api")

    conflicts("+jasper +openjpeg", msg="Either Jasper or OpenJPEG should be used, not both")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define("BUILD_SHARED_LIBS", self.spec.satisfies("libs=shared")),
            self.define("BUILD_STATIC_LIBS", self.spec.satisfies("libs=static")),
            self.define_from_variant("USE_AEC", "aec"),
            self.define_from_variant("USE_PNG", "png"),
            self.define_from_variant("USE_Jasper", "jasper"),
            self.define_from_variant("USE_OpenJPEG", "openjpeg"),
            self.define_from_variant("PTHREADS", "pthreads"),
            self.define_from_variant("UTILS", "utils"),
            self.define_from_variant("BUILD_G2C", "build_v2_api"),
            self.define("BUILD_TESTING", self.run_tests),
        ]

        return args

    def setup_run_environment(self, env):
        if self.spec.satisfies("@:1.6"):
            shared = False
        else:
            shared = self.spec.satisfies("libs=shared")
        lib = find_libraries("libg2c", root=self.prefix, shared=shared, recursive=True)
        env.set("G2C_LIB", lib[0])
        env.set("G2C_INC", join_path(self.prefix, "include"))

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
