# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ip(CMakePackage):
    """The NCEP general interpolation library (iplib) contains Fortran 90
    subprograms to be used for interpolating between nearly all grids used at
    NCEP. This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-ip"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-ip/archive/refs/tags/v3.3.3.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-ip"

    maintainers("AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA")

    version("develop", branch="develop")
    version("5.1.0", sha256="5279f11f4c12db68ece74cec392b7a2a6b5166bc505877289f34cc3149779619")
    version("5.0.0", sha256="54b2987bd4f94adc1f7595d2a384e646019c22d163bcd30840a916a6abd7df71")
    version("4.4.0", sha256="858d9201ce0bc4d16b83581ef94a4a0262f498ed1ea1b0535de2e575da7a8b8c")
    version("4.3.0", sha256="799308a868dea889d2527d96a0405af7b376869581410fe4cff681205e9212b4")
    # Note that versions 4.0-4.2 contain constants_mod module, and should not be used when
    # also compiling with packages containing Fortran modules of the same name, namely, FMS.
    version("4.2.0", sha256="9b9f47106822044ff224c6dfd9f140c146dffc833904f2a0c5db7b5d8932e39e")
    version("4.1.0", sha256="b83ca037d9a5ad3eb0fb1acfe665c38b51e01f6bd73ce9fb8bb2a14f5f63cdbe")
    version("4.0.0", sha256="a2ef0cc4e4012f9cb0389fab6097407f4c623eb49772d96eb80c44f804aa86b8")
    version(
        "3.3.3",
        sha256="d5a569ca7c8225a3ade64ef5cd68f3319bcd11f6f86eb3dba901d93842eb3633",
        preferred=True,
    )

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("openmp", description="Enable OpenMP threading", default=True)
    variant("pic", default=True, description="Build with position-independent-code")
    variant("shared", default=False, description="Build shared library", when="@4.1:")
    variant(
        "precision",
        default=("4", "d"),
        values=("4", "d"),
        multi=True,
        description="Set precision (_4/_d library versions)",
        when="@4.1",
    )
    variant(
        "precision",
        default=("4", "d"),
        values=("4", "d", "8"),
        multi=True,
        description="Set precision (_4/_d/_8 library versions)",
        when="@4.2:",
    )
    variant(
        "deprecated",
        default=False,
        description="Build deprecated spectral interpolation functions",
        when="@5.0:",
    )

    conflicts("+shared ~pic")

    depends_on("sp", when="@:4")
    depends_on("sp@:2.3.3", when="@:4.0")
    depends_on("sp precision=4", when="@4.1:4 precision=4")
    depends_on("sp precision=d", when="@4.1:4 precision=d")
    depends_on("sp precision=8", when="@4.1:4 precision=8")
    depends_on("lapack", when="@5.1:")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP", "openmp"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

        if self.spec.satisfies("@4:"):
            args.append(self.define("BUILD_TESTING", self.run_tests))
        else:
            args.append(self.define("ENABLE_TESTS", "NO"))

        if self.spec.satisfies("@4.1:"):
            args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
            args.append(self.define("BUILD_4", self.spec.satisfies("precision=4")))
            args.append(self.define("BUILD_D", self.spec.satisfies("precision=d")))

        if self.spec.satisfies("@4.2:"):
            args.append(self.define("BUILD_8", self.spec.satisfies("precision=8")))

        if self.spec.satisfies("@5:"):
            args.append(self.define_from_variant("BUILD_DEPRECATED", "deprecated"))

        if self.spec.satisfies("@5.1:"):
            # Use the LAPACK provider set by Spack even if the compiler supports native BLAS
            bla_vendors = {"openblas": "OpenBLAS"}
            lapack_provider = self.spec["lapack"].name
            if lapack_provider in bla_vendors.keys():
                bla_vendor = bla_vendors[lapack_provider]
            else:
                bla_vendor = "All"
            args.append(self.define("BLA_VENDOR", bla_vendor))

        return args

    def setup_run_environment(self, env):
        suffixes = (
            self.spec.variants["precision"].value
            if self.spec.satisfies("@4.1:")
            else ("4", "8", "d")
        )
        shared = False if self.spec.satisfies("@:4.0") else self.spec.satisfies("+shared")
        for suffix in suffixes:
            lib = find_libraries(
                "libip_" + suffix, root=self.prefix, shared=shared, recursive=True
            )
            env.set("IP_LIB" + suffix, lib[0])
            env.set("IP_INC" + suffix, join_path(self.prefix, "include_" + suffix))

    @when("@4:")
    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
