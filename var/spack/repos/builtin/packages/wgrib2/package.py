# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *

variant_map_common = {
    "netcdf3": "USE_NETCDF3",
    "netcdf4": "USE_NETCDF4",
    "mysql": "USE_MYSQL",
    "udf": "USE_UDF",
    "regex": "USE_REGEX",
    "tigge": "USE_TIGGE",
    "proj4": "USE_PROJ4",
    "aec": "USE_AEC",
    "g2c": "USE_G2CLIB",
    "png": "USE_PNG",
    "jasper": "USE_JASPER",
    "openmp": "USE_OPENMP",
    "wmo_validation": "USE_WMO_VALIDATION",
    "ipolates": "USE_IPOLATES",
    "disable_alarm": "DISABLE_ALARM",
    "fortran_api": "MAKE_FTN_API",
    "disable_stat": "DISABLE_STAT",
    "openjpeg": "USE_OPENJPEG",
}

variant_map_makefile = {"spectral": "USE_SPECTRAL"}

variant_map_cmake = {
    "netcdf": "USE_NETCDF",
    "disable_timezone": "DISABLE_TIMEZONE",
    "enable_docs": "ENABLE_DOCS",
}

variant_map_makefile.update(variant_map_common)
variant_map_cmake.update(variant_map_common)


class Wgrib2(MakefilePackage, CMakePackage):
    """Utility for interacting with GRIB2 files"""

    homepage = "https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2"
    url = "https://github.com/NOAA-EMC/wgrib2/archive/refs/tags/v3.5.0.tar.gz"
    git = "https://github.com/NOAA-EMC/wgrib2.git"

    maintainers(
        "AlysonStahl-NOAA", "t-brown", "AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett"
    )

    build_system(
        conditional("cmake", when="@3.2:"), conditional("makefile", when="@:3.1"), default="cmake"
    )

    version("develop", branch="develop")
    version("3.5.0", sha256="b27b48228442a08bddc3d511d0c6335afca47252ae9f0e41ef6948f804afa3a1")
    version("3.4.0", sha256="ecbce2209c09bd63f1bca824f58a60aa89db6762603bda7d7d3fa2148b4a0536")
    version("3.3.0", sha256="010827fba9c31f05807e02375240950927e9e51379e1444388153284f08f58e2")
    version("3.2.0", sha256="ac3ace77a32c2809cbc4538608ad64aabda2c9c1e44e7851da79764a6eb3c369")
    version(
        "3.1.1",
        sha256="9236f6afddad76d868c2cfdf5c4227f5bdda5e85ae40c18bafb37218e49bc04a",
        extension="tar.gz",
    )
    version(
        "3.1.0",
        sha256="5757ef9016b19ae87491918e0853dce2d3616b14f8c42efe3b2f41219c16b78f",
        extension="tar.gz",
    )
    version(
        "2.0.8",
        sha256="5e6a0d6807591aa2a190d35401606f7e903d5485719655aea1c4866cc2828160",
        extension="tar.gz",
    )
    version(
        "2.0.7",
        sha256="d7f1a4f9872922c62b3c7818c022465532cca1f5666b75d3ac5735f0b2747793",
        extension="tar.gz",
    )

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    def url_for_version(self, version):
        if version >= Version("3.2.0"):
            url_fmt = "https://github.com/NOAA-EMC/wgrib2/archive/refs/tags/v{0}.tar.gz"
        else:
            url_fmt = "https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v{0}"
        return url_fmt.format(version)

    variant(
        "netcdf3",
        default=True,
        description="Link in netcdf3 library to write netcdf3 files",
        when="@:3.1",
    )
    variant(
        "netcdf4",
        default=False,
        description="Link in netcdf4 library to write netcdf3/4 files",
        when="@:3.3",
    )
    variant(
        "netcdf",
        default=False,
        description="Link in netcdf4 library to write netcdf3/4 files",
        when="@3.4:",
    )
    variant("ipolates", default=False, description="Use to interpolate to new grids")
    variant(
        "spectral", default=False, description="Spectral interpolation in -new_grid", when="@:3.1"
    )
    #   Not currently working for @3.2:
    variant(
        "fortran_api",
        default=True,
        description="Make wgrib2api which allows fortran code to read/write grib2",
    )
    #   Not currently working for @3.2:
    #    variant("lib", default=True, description="Build library", when="@3.2:")
    variant(
        "mysql",
        default=False,
        description="Link in interface to MySQL to write to mysql database",
        when="@:3.1",
    )
    variant(
        "udf",
        default=False,
        description="Add commands for user-defined functions and shell commands",
    )
    variant("regex", default=True, description="Use regular expression library (POSIX-2)")
    variant("tigge", default=True, description="Ability for TIGGE-like variable names")
    variant(
        "proj4",
        default=False,
        description="The proj4 library is used to verify gctpc.",
        when="@:3.1",
    )
    variant(
        "aec", default=True, description="Use the libaec library for packing with GRIB2 template"
    )
    variant(
        "g2c",
        default=False,
        description="Include NCEP g2clib (mainly for testing purposes)",
        when="@:3.1",
    )
    variant(
        "disable_timezone", default=False, description="Some machines do not support timezones"
    )
    variant(
        "disable_alarm",
        default=False,
        description="Some machines do not support the alarm to terminate wgrib2",
    )
    variant("png", default=True, description="PNG encoding")
    variant("jasper", default=True, description="JPEG compression using Jasper")
    variant("openmp", default=True, description="OpenMP parallelization")
    variant("wmo_validation", default=False, description="WMO validation")
    #    variant("shared", default=False, description="Enable shared library", when="+lib")
    variant("disable_stat", default=False, description="Disable POSIX feature", when="@:3.1")
    variant("openjpeg", default=False, description="Enable OpenJPEG")
    variant(
        "enable_docs", default=False, description="Build doxygen documentation", when="@3.4.0:"
    )

    conflicts("+netcdf3", when="+netcdf4")
    conflicts("+netcdf3", when="+netcdf")
    conflicts("+openmp", when="%apple-clang")

    depends_on("ip@5.1:", when="@3.5: +ipolates")
    depends_on("lapack", when="@3.5: +ipolates")
    depends_on("libaec@1.0.6:", when="@3.2: +aec")
    depends_on("netcdf-c", when="@3.2: +netcdf4")
    depends_on("jasper@:2", when="@3.2:3.4 +jasper")
    depends_on("g2c", when="@3.5: +jasper")
    depends_on("zlib-api", when="@3.2: +png")
    depends_on("libpng", when="@3.2: +png")
    depends_on("openjpeg", when="@3.2:3.4 +openjpeg")
    depends_on("g2c +openjpeg", when="@3.5: +openjpeg")
    requires("^g2c@1.9:", when="@3.5: ^g2c")

    @when("@:2 ^gmake@4.2:")
    def patch(self):
        filter_file(r"\\#define", "#define", "makefile")

    # Use Spack compiler wrapper flags
    def inject_flags(self, name, flags):
        if name == "cflags":
            if self.spec.compiler.name == "apple-clang":
                flags.append("-Wno-error=implicit-function-declaration")

            # When mixing Clang/gfortran need to link to -lgfortran
            # Find this by searching for gfortran/../lib
            if self.spec.compiler.name in ["apple-clang", "clang"]:
                if "gfortran" in self.compiler.fc:
                    output = Executable(self.compiler.fc)("-###", output=str, error=str)
                    libdir = re.search("--libdir=(.+?) ", output).group(1)
                    flags.append("-L{}".format(libdir))

        return (flags, None, None)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    # Disable parallel build
    parallel = False

    def cmake_args(self):
        args = [self.define_from_variant(variant_map_cmake[k], k) for k in variant_map_cmake]
        #        args.append(self.define_from_variant("BUILD_LIB", "lib"))
        #        args.append(self.define_from_variant("BUILD_SHARED_LIB", "shared"))

        return args


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    # Disable parallel build
    parallel = False

    flag_handler = inject_flags

    def url_for_version(self, version):
        url = "https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v{}"
        return url.format(version)

    def edit(self, pkg, spec, prefix):
        makefile = FileFilter("makefile")

        # ifort no longer accepts -openmp
        makefile.filter(r"-openmp", "-qopenmp")
        makefile.filter(r"-Wall", " ")
        makefile.filter(r"-Werror=format-security", " ")

        # clang doesn"t understand --fast-math
        if spec.satisfies("%clang") or spec.satisfies("%apple-clang"):
            makefile.filter(r"--fast-math", "-ffast-math")

        for variant_name, makefile_option in variant_map_makefile.items():
            value = int(spec.variants[variant_name].value)
            makefile.filter(r"^%s=.*" % makefile_option, "{}={}".format(makefile_option, value))

    def setup_build_environment(self, env):
        if self.spec.compiler.name in ["oneapi", "intel"]:
            comp_sys = "intel_linux"
        elif self.spec.compiler.name in ["gcc", "clang", "apple-clang"]:
            comp_sys = "gnu_linux"

        env.set("COMP_SYS", comp_sys)

    def build(self, pkg, spec, prefix):
        make("-j1")

        # Move wgrib2 executable to a tempoary directory
        mkdir("install")
        mkdir(join_path("install", "bin"))
        move(join_path("wgrib2", "wgrib2"), join_path("install", "bin"))

        # Build wgrib2 library by disabling all options
        # and enabling only MAKE_FTN_API=1
        if "+fortran_api" in spec:
            make("clean")
            make("deep-clean")
            makefile = FileFilter("makefile")

            # Disable all options
            for variant_name, makefile_option in variant_map_makefile.items():
                value = 0
                makefile.filter(
                    r"^%s=.*" % makefile_option, "{}={}".format(makefile_option, value)
                )

            # Need USE_REGEX in addition to MAKE_FTN_API to build lib
            makefile.filter(r"^MAKE_FTN_API=.*", "MAKE_FTN_API=1")
            makefile.filter(r"^USE_REGEX=.*", "USE_REGEX=1")
            make("lib", "-j1")
            mkdir(join_path("install", "lib"))
            mkdir(join_path("install", "include"))

            move(join_path("lib", "libwgrib2.a"), join_path("install", "lib"))
            move(join_path("lib", "wgrib2api.mod"), join_path("install", "include"))
            move(join_path("lib", "wgrib2lowapi.mod"), join_path("install", "include"))

    def install(self, pkg, spec, prefix):
        install_tree("install/", prefix)
