# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.netlib_scalapack import ScalapackBase


class Amdscalapack(ScalapackBase):
    """
    ScaLAPACK is a library of high-performance linear algebra routines
    for parallel distributed memory machines. It depends on external
    libraries including BLAS and LAPACK for Linear Algebra computations.

    AMD's optimized version of ScaLAPACK enables using BLIS and
    LibFLAME library that have optimized dense matrix functions and
    solvers for AMD EPYC processor family CPUs.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-ScaLAPACK license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/scalapack/eula/scalapack-libraries-4-2-eula.html
    https://www.amd.com/en/developer/aocl/scalapack/eula/scalapack-libraries-eula.html
    """

    _name = "amdscalapack"
    homepage = "https://www.amd.com/en/developer/aocl/scalapack.html"
    git = "https://github.com/amd/aocl-scalapack"

    maintainers("amd-toolchain-support")

    license("BSD-3-Clause-Open-MPI")
    version(
        "5.0",
        sha256="a33cf16c51cfd65c7acb5fbdb8884a5c147cdefea73931b07863c56d54f812cc",
        preferred=True,
    )
    version("4.2", sha256="c6e9a846c05cdc05252b0b5f264164329812800bf13f9d97c77114dc138e6ccb")
    version("4.1", sha256="b2e51c3604e5869d1faaef2e52c92071fcb3de1345aebb2ea172206622067ad9")
    version("4.0", sha256="f02913b5984597b22cdb9a36198ed61039a1bf130308e778dc31b2a7eb88b33b")
    version("3.2", sha256="9e00979bb1be39d627bdacb01774bc043029840d542fafc934d16fec3e3b0892")
    version("3.1", sha256="4c2ee2c44644a0feec0c6fc1b1a413fa9028f14d7035d43a398f5afcfdbacb98")
    version("3.0", sha256="6e6f3578f44a8e64518d276e7580530599ecfa8729f568303ed2590688e7096f")
    version("2.2", sha256="2d64926864fc6d12157b86e3f88eb1a5205e7fc157bf67e7577d0f18b9a7484c")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("amdblis", when="^[virtuals=blas] amdblis")
    depends_on("amdlibflame", when="^[virtuals=lapack] amdlibflame")

    variant("ilp64", default=False, description="Build with ILP64 support")

    conflicts("+ilp64", when="@:3.0", msg="ILP64 is supported from 3.1 onwards")
    requires("target=x86_64:", msg="AMD scalapack available only on x86_64")

    patch("clang-hollerith.patch", when="@=4.0 %clang@16:")

    def patch(self):
        # Flang-New gets confused and thinks it finds Hollerith constants
        if self.spec.satisfies("%clang@16:"):
            filter_file("-cpp", "", "CMakeLists.txt")
        # remove the C-style comments in header file that cause issues with flang
        if self.spec.satisfies("@4.2: %clang@18:"):
            which("sed")(
                "-i",
                "1,23d",
                join_path(self.stage.source_path, "FRAMEWORK", "SL_Context_fortran_include.h"),
            )

    def url_for_version(self, version):
        vers = "https://github.com/amd/{0}/archive/{1}.tar.gz"
        if version >= Version("3.1"):
            return vers.format("aocl-scalapack", version)
        else:
            return vers.format("scalapack", version)

    def flag_handler(self, name, flags):
        (flags, _, _) = super().flag_handler(name, flags)
        # remove a flag set in ScalapackBase that is not working
        if self.spec.satisfies("%gcc@14:"):
            if "-std=gnu89" in flags:
                flags.remove("-std=gnu89")
        return (flags, None, None)

    def cmake_args(self):
        """cmake_args function"""
        args = super().cmake_args()
        spec = self.spec

        if spec.satisfies("%gcc@10:"):
            args.extend(["-DCMAKE_Fortran_FLAGS={0}".format("-fallow-argument-mismatch")])

        if spec.satisfies("%clang@16:"):
            flags = "-cpp -fno-implicit-none"
            if spec.satisfies("%clang@18"):
                flags += " -flang-experimental-polymorphism"
            if spec.satisfies("%clang@18:"):
                flags += " -I{0}".format(join_path(self.stage.source_path, "FRAMEWORK"))
            args.extend(["-DCMAKE_Fortran_FLAGS={0}".format(flags)])

        if spec.satisfies("@2.2"):
            args.extend(
                [
                    "-DUSE_DOTC_WRAPPER:BOOL=%s"
                    % ("ON" if spec.satisfies("%aocc ^amdblis") else "OFF")
                ]
            )

        # -DENABLE_ILP64:BOOL=ON
        args.extend([self.define_from_variant("ENABLE_ILP64", "ilp64")])

        # -DUSE_F2C:BOOL=ON
        args.extend([self.define("USE_F2C", spec.satisfies("@:3.0"))])

        if self.spec.satisfies("%clang@16:") or self.spec.satisfies("%aocc@4.1.0:"):
            c_flags = []
            c_flags.append("-Wno-implicit-function-declaration")
            c_flags.append("-Wno-deprecated-non-prototype")
            c_flags.append("-Wno-incompatible-pointer-types")
            args.append(self.define("CMAKE_C_FLAGS", " ".join(c_flags)))
        elif self.spec.satisfies("%gcc@14:"):
            args.append(self.define("CMAKE_C_FLAGS", "-Wno-incompatible-pointer-types"))

        # link libflame library
        args.extend(["-DLAPACK_LIBRARIES={0}".format(self.spec["lapack"].libs)])

        args.extend(
            [
                "-DLAPACK_FOUND=true",
                "-DUSE_OPTIMIZED_LAPACK_BLAS=true",
                "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            ]
        )

        return args

    def setup_dependent_run_environment(self, env, dependent_spec):
        if self.spec.external:
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
