# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sp(CMakePackage):
    """The spectral transform library splib contains FORTRAN subprograms
    to be used for a variety of spectral transform functions. This is
    part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sp"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-sp/archive/refs/tags/v2.3.3.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-sp"

    maintainers("AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA")

    version("develop", branch="develop")
    version("2.5.0", sha256="aec475ccb5ccf7c5a758dfb699626f2be78a22729a9d8d5e0a286db6a3213a51")
    version("2.4.0", sha256="dbb4280e622d2683b68a28f8e3837744adf9bbbb1e7940856e8f4597f481c708")
    version("2.3.3", sha256="c0d465209e599de3c0193e65671e290e9f422f659f1da928505489a3edeab99f")

    depends_on("fortran", type="build")

    variant("shared", default=False, description="Build shared library", when="@2.4:")
    variant("openmp", default=False, description="Use OpenMP threading")
    variant("pic", default=False, description="Enable position-independent code (PIC)")
    variant(
        "precision",
        default=("4", "d"),
        values=("4", "d", "8"),
        multi=True,
        description="Library versions: 4=4-byte reals, d=8-byte reals, 8=8-byte ints and reals",
        when="@2.4:",
    )

    def setup_run_environment(self, env):
        if self.spec.satisfies("@2.4:"):
            suffixes = self.spec.variants["precision"].value
        else:
            suffixes = ("4", "d", "8")

        for suffix in suffixes:
            lib = find_libraries(
                "libsp_" + suffix,
                root=self.prefix,
                shared=self.spec.satisfies("+shared"),
                recursive=True,
            )
            env.set("SP_LIB" + suffix, lib[0])
            env.set("SP_INC" + suffix, "include_" + suffix)

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"))
        args.append(self.define_from_variant("OPENMP", "openmp"))
        args.append(self.define("BUILD_4", self.spec.satisfies("precision=4")))
        args.append(self.define("BUILD_D", self.spec.satisfies("precision=d")))
        args.append(self.define("BUILD_8", self.spec.satisfies("precision=8")))
        args.append(self.define("BUILD_DEPRECATED", False))
        if self.spec.satisfies("@2.4:"):
            args.append(self.define("BUILD_TESTING", self.run_tests))
        return args

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
