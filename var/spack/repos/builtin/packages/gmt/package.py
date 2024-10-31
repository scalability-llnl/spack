# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


class Gmt(CMakePackage, AutotoolsPackage):
    """GMT (Generic Mapping Tools) is an open source collection of about 80
    command-line tools for manipulating geographic and Cartesian data sets
    (including filtering, trend fitting, gridding, projecting, etc.) and
    producing PostScript illustrations ranging from simple x-y plots via
    contour maps to artificially illuminated surfaces and 3D perspective views.
    """

    homepage = "https://www.generic-mapping-tools.org/"
    url = "https://github.com/GenericMappingTools/gmt/archive/6.1.0.tar.gz"
    git = "https://github.com/GenericMappingTools/gmt.git"

    maintainers("adamjstewart")

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("6.4.0", sha256="c39d23dbc8a85416457946f6b93c2b9a5f039f092453e7f4b1aaf88d4a288300")
    version("6.3.0", sha256="48712279da8228a7960f36fd4b7b04cc1a66489c37b2a5c03f8336a631aa3b24")
    version("6.2.0", sha256="b70786ca5ba7d1293acc4e901a0f82e1300d368b61009ef87f771f4bc99d058a")
    version("6.1.1", sha256="4cb17f42ff10b8f5fe372956c23f1fa3ca21a8e94933a6c614894f0be33427c1")
    version("6.1.0", sha256="f76ad7f444d407dfd7e5762644eec3a719c6aeb06d877bf746fe51abd79b1a9e")
    version("6.0.0", sha256="7a733e670f01d99f8fc0da51a4337320d764c06a68746621f83ccf2e3453bcb7")
    version("5.4.4", sha256="b593dfb101e6507c467619f3d2190a9f78b09d49fe2c27799750b8c4c0cd2da0")
    version(
        "4.5.18",
        sha256="27c30b516c317fed8e44efa84a0262f866521d80cfe76a61bf12952efb522b63",
        url="ftp://ftp.soest.hawaii.edu/gmt/gmt-4.5.18-src.tar.bz2",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "ghostscript",
        default=False,
        description="Ability to convert PostScript plots to PDF and rasters",
    )
    variant("geos", default=False, description="Ability to buffer lines and polygons")
    variant("pcre", default=False, description="Regular expression support")
    variant("fftw", default=False, description="Fast FFTs")
    variant("glib", default=False, description="GTHREAD support")
    variant("lapack", default=False, description="Fast matrix inversion")
    variant("blas", default=False, description="Fast matrix multiplications")
    variant("graphicsmagick", default=False, description="Convert images to animated GIFs")
    variant("ffmpeg", default=False, description="Convert images to videos")

    # https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md

    # Build system
    build_system(
        conditional("cmake", when="@5.0.1:"),
        conditional("autotools", when="@:5.0.0"),
        default="cmake",
    )

    # Required dependencies
    with when("build_system=cmake"):
        generator("ninja")
        depends_on("cmake@2.8.12:", type="build")

    depends_on("netcdf-c@4:")
    depends_on("curl", when="@5.4:")
    depends_on("gdal")

    # Optional dependencies
    depends_on("ghostscript", when="+ghostscript")
    depends_on("pcre2", when="+pcre")
    depends_on("fftw@3.3:", when="+fftw")
    depends_on("glib@2.32:", when="+glib")
    depends_on("lapack", when="+lapack")
    depends_on("blas", when="+blas")
    depends_on("graphicsmagick", when="+graphicsmagick")
    depends_on("ffmpeg", when="+ffmpeg")

    depends_on("graphicsmagick", type="test")
    depends_on("py-dvc", type="test")

    resource(
        name="gshhg",
        url="https://github.com/GenericMappingTools/gshhg-gmt/releases/download/2.3.7/gshhg-gmt-2.3.7.tar.gz",
        sha256="9bb1a956fca0718c083bef842e625797535a00ce81f175df08b042c2a92cfe7f",
        destination="share",
        placement="gshhg",
    )
    resource(
        name="dcw",
        url="https://github.com/GenericMappingTools/dcw-gmt/releases/download/2.1.1/dcw-gmt-2.1.1.tar.gz",
        sha256="d4e208dca88fbf42cba1bb440fbd96ea2f932185c86001f327ed0c7b65d27af1",
        destination="share",
        placement="dcw",
    )

    # https://github.com/spack/spack/issues/26661
    conflicts(
        "%gcc@11:",
        when="@:5",
        msg="GMT 5 cannot be built with GCC 11+, try a newer GMT or older GCC",
    )

    # https://github.com/GenericMappingTools/gmt/pull/3603
    patch("regexp.patch", when="@6.1.0")
    patch("type.patch", when="@4")

    executables = ["^gmt-config$"]

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)("--version", output=str, error=str).rstrip()


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("NETCDF_CONFIG", spec["netcdf-c"].prefix.bin.join("nc-config")),
            self.define("GDAL_CONFIG", spec["gdal"].prefix.bin.join("gdal-config")),
            self.define("PCRE_CONFIG", ""),
            self.define("GSHHG_PATH", "gshhg"),
            self.define("DCW_PATH", "dcw"),
        ]

        if spec.satisfies("+ghostscript"):
            args.append(self.define("GS", spec["ghostscript"].prefix.bin.gs))

        if spec.satisfies("+geos"):
            args.append(self.define("GEOS_CONFIG", spec["geos"].prefix.bin.join("geos-config")))

        if spec.satisfies("+pcre"):
            args.append(self.define("PCRE2_CONFIG", spec["pcre2"].prefix.bin.join("pcre2-config")))

        if spec.satisfies("+fftw"):
            args.extend(
                [
                    self.define("FFTW3_INCLUDE_DIR", spec["fftw"].headers.directories[0]),
                    self.define("FFTW3F_LIBRARY", spec["fftw"].libs.directories[0]),
                ]
            )

        if spec.satisfies("+glib"):
            args.extend(
                [
                    self.define("GLIB_INCLUDE_DIR", spec["glib"].headers.directories[0]),
                    self.define("GLIB_LIBRARIES", spec["glib"].libs[0]),
                ]
            )

        if spec.satisfies("graphicsmagick"):
            args.extend(
                [
                    self.define("GM", spec["graphicsmagick"].prefix.bin.gm),
                    self.define("GRAPHICSMAGICK", spec["graphicsmagick"].prefix.bin.gm),
                ]
            )

        if spec.satisfies("+ffmpeg"):
            args.append(self.define("FFMPEG", spec["ffmpeg"].prefix.bin.ffmpeg))

        return args


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        return [
            "--enable-netcdf={0}".format(self.spec["netcdf-c"].prefix),
            "--enable-gdal",
            "--enable-shared",
            "--without-x",
        ]

    def build(self, pkg, spec, prefix):
        # Building in parallel results in dozens of errors like:
        # *** No rule to make target `../libgmtps.so', needed by `pssegyz'.
        make(parallel=False)

    def install(self, pkg, spec, prefix):
        # Installing in parallel results in dozens of errors like:
        # /usr/bin/install: cannot create directory '...': File exists
        make("install", parallel=False)
