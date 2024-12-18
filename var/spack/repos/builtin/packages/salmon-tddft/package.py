# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class SalmonTddft(CMakePackage):
    """SALMON is an open-source computer program for ab-initio
    quantum-mechanical calculations of electron dynamics at the nanoscale
    that takes place in various situations of light-matter interactions.
    It is based on time-dependent density functional theory, solving
    time-dependent Kohn-Sham equation in real time and real space
    with norm-conserving pseudopotentials."""

    homepage = "https://salmon-tddft.jp"
    url = "https://salmon-tddft.jp/download/SALMON-v.2.0.0.tar.gz"

    license("BSD-3-Clause-Open-MPI")

    version("2.0.0", sha256="c3bb80bc5d338cba21cd8f345acbf2f2d81ef75af069a0a0ddbdc0acf358456c")
    version("1.2.1", sha256="a5045149e49abe9dd9edefe00cd1508a1323081bc3d034632176b728effdbaeb")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI")
    variant("libxc", default=False, description="Enable libxc")
    variant("scalapack", default=False, description="Enable scalapack")
    variant("eigenexa", default=False, description="Enable eigenexa")
    variant(
        "manycore",
        default=False,
        description="Enable optimization of reduction for many-core processor",
    )
    variant(
        "current_processing",
        default=False,
        description="Enable preprocessing of the current computation in RT",
    )

    depends_on("cmake@3.14:", type="build")
    depends_on("mpi", type="link", when="+mpi")
    depends_on("scalapack", type="link", when="+scalapack")
    depends_on("eigenexa", type="link", when="+eigenexa")
    depends_on("lapack", type="link")
    depends_on("libxc", type="link", when="+libxc")
    depends_on("libxc@:4.9", type="link", when="@:1.9.9 +libxc")

    conflicts("+scalapack", when="~mpi")
    conflicts("+eigenexa", when="@:1.9.9")
    conflicts("+eigenexa", when="~scalapack")
    conflicts("+manycore", when="@2.0.0:")
    conflicts("+current_processing", when="@2.0.0:")

    patch("fjmpi.patch", when="@2.0.0: %fj")
    patch("v2.0.libxc-5.0.patch", when="@2.0.0 +libxc")
    patch("cmakefix.patch", when="+scalapack")

    def cmake_args(self):
        define_from_variant = self.define_from_variant
        spec = self.spec
        define = self.define
        args = [
            define_from_variant("USE_SCALAPACK", "scalapack"),
            define_from_variant("USE_EIGENEXA", "eigenexa"),
            define_from_variant("USE_MPI", "mpi"),
            define_from_variant("USE_LIBXC", "libxc"),
            define_from_variant("REDUCE_FOR_MANYCORE", "manycore"),
            define_from_variant("CURRENT_PREPROCESSING", "current_processing"),
        ]
        if spec.satisfies("+mpi"):
            args.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                ]
            )
        if spec.satisfies("+scalapack"):
            math_libs = spec["scalapack"].libs + spec["lapack"].libs + spec["blas"].libs
            if spec.satisfies("@2.0:"):
                args.append(define("ScaLAPACK_VENDOR_FLAGS", math_libs.ld_flags))
            else:
                args.extend(
                    [
                        define("BLACS_LINKER_FLAGS", math_libs.ld_flags),
                        define("BLACS_LIBRARIES", math_libs.libraries),
                        define("ScaLAPACK_LINKER_FLAGS", math_libs.ld_flags),
                        define("ScaLAPACK_LIBRARIES", math_libs.libraries),
                    ]
                )
        if spec.satisfies("^fujitsu-mpi"):
            args.append(define("USE_FJMPI", True))
        else:
            args.append(define("USE_FJMPI", False))
        if spec.satisfies("%fj"):
            args.append(self.define("CMAKE_Fortran_MODDIR_FLAG", "-M"))
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "fflags":
            if self.spec.satisfies("%gcc"):
                flags.append("-ffree-line-length-none")
        return (None, None, flags)
