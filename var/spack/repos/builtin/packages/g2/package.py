# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class G2(CMakePackage):
    """Utilities for coding/decoding GRIB2 messages. This library contains
    Fortran 90 decoder/encoder routines for GRIB edition 2, as well as
    indexing/searching utility routines.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-g2"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-g2/archive/refs/tags/v3.4.3.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-g2"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("3.5.1", sha256="a9acdb5d23eca532838f21c4a917727ac85851fc9e1f100d65a6f27c1a563998")
    version("3.5.0", sha256="3ff59a705bedf56061bba2d667a04391d82701847f93ea5fa1c1d3bd335d07da")
    version("3.4.9", sha256="6edc33091f6bd2acb191182831499c226a1c3992c3acc104d6363528b12dfbae")
    version("3.4.8", sha256="071a6f799c4c4fdfd5d0478152a0cbb9d668d12d71c78d5bda71845fc5580a7f")
    version("3.4.7", sha256="d6530611e3a515122f11ed4aeede7641f6f8932ef9ee0d4828786572767304dc")
    version("3.4.6", sha256="c4b03946365ce0bacf1e10e8412a5debd72d8671d1696aa4fb3f3adb119175fe")
    version("3.4.5", sha256="c18e991c56964953d778632e2d74da13c4e78da35e8d04cb742a2ca4f52737b6")
    version("3.4.3", sha256="679ea99b225f08b168cbf10f4b29f529b5b011232f298a5442ce037ea84de17c")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("pic", default=True, description="Build with position-independent-code")
    variant(
        "precision",
        default=("4", "d"),
        values=("4", "d"),
        multi=True,
        description="Set precision (_4/_d library versions)",
        when="@3.4.6:",
    )
    variant("w3emc", default=True, description="Enable GRIB1 through w3emc", when="@3.4.6:")
    variant("shared", default="False", description="Build shared library", when="@3.4.7:")
    variant("openmp", default=False, description="Use OpenMP multithreading", when="@develop")
    variant("utils", default=False, description="Build grib utilities", when="@develop")
    variant(
        "g2c_compare",
        default=False,
        description="Enable copygb2 tests using g2c_compare",
        when="@develop",
    )

    depends_on("jasper@:2.0.32", when="@:3.4.7")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("zlib-api", when="@develop")
    depends_on("bacio", when="@3.4.6:")
    depends_on("ip", when="@develop")
    requires("^ip precision=d", when="^ip@4.1:")
    depends_on("sp", when="^ip@:4")
    requires("^sp precision=d", when="^ip@:4 ^sp@2.4:")
    depends_on("g2c@1.8: +utils", when="+g2c_compare")
    with when("+w3emc"):
        depends_on("w3emc")
        depends_on("w3emc precision=4", when="precision=4")
        depends_on("w3emc precision=d", when="precision=d")
        depends_on("w3emc +extradeps", when="+utils")
        depends_on("w3emc precision=4,d", when="+utils")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP", "openmp"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("BUILD_WITH_W3EMC", "w3emc"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_4", self.spec.satisfies("precision=4")),
            self.define("BUILD_D", self.spec.satisfies("precision=d")),
            self.define_from_variant("G2C_COMPARE", "g2c_compare"),
            self.define_from_variant("BUILD_UTILS", "utils"),
        ]

        return args

    def setup_run_environment(self, env):
        precisions = (
            self.spec.variants["precision"].value if self.spec.satisfies("@3.4.6:") else ("4", "d")
        )
        for suffix in precisions:
            lib = find_libraries(
                "libg2_" + suffix,
                root=self.prefix,
                shared=self.spec.satisfies("+shared"),
                recursive=True,
            )
            env.set("G2_LIB" + suffix, lib[0])
            env.set("G2_INC" + suffix, join_path(self.prefix, "include_" + suffix))

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
