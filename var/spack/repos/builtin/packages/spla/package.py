# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spla(CMakePackage):
    """Specialized Parallel Linear Algebra, providing distributed GEMM
    functionality for specific matrix distributions with optional GPU
    acceleration."""

    homepage = "https://github.com/eth-cscs/spla"
    url = "https://github.com/eth-cscs/spla/archive/v1.0.0.tar.gz"
    git = "https://github.com/eth-cscs/spla.git"

    maintainers("AdhocMan", "haampie")

    license("BSD-3-Clause")

    version("1.6.1", sha256="62b51e6ce05c41cfc1c6f6600410f9549a209c50f0331e1db41047f94493e02f")
    version("1.6.0", sha256="917c24e2a768499967eba47b2cc2475df9fabee327b7821d24970b6a08055c09")
    version("1.5.5", sha256="bc0c366e228344b1b2df55b9ce750d73c1165380e512da5a04d471db126d66ce")
    version("1.5.4", sha256="de30e427d24c741e2e4fcae3d7668162056ac2574afed6522c0bb49d6f1d0f79")
    version("1.5.3", sha256="527c06e316ce46ec87309a16bfa4138b1abad23fd276fe789c78a2de84f05637")
    version("1.5.2", sha256="344c34986dfae182ec2e1eb539c9a57f75683aaa7a61a024fd0c594d81d97016")
    version("1.5.1", sha256="2021a30b7cbb10bd660e5d94e1cc7bc6a428c87ea507e09d1e57e455685da421")
    version("1.5.0", sha256="bea782d46ce615e1c40efc2bfb19d95e3b59f332fc9ca83ac7e6684b8ac2dd93")
    version("1.4.0", sha256="364a9fe759fddec8a0839cf79f1cf0619fc36f4d4c15f1c2b1f437249d7840c6")
    version("1.3.0", sha256="ff05a22bd655607ff941f3228ac8605a813e1eec6eaa49fbcf7b58a3a4cf5f00")
    version("1.2.1", sha256="4d7237f752dc6257778c84ee19c9635072b1cb8ce8d9ab6e34a047f63a736b29")
    version("1.2.0", sha256="96ddd13c155ef3d7e40f87a982cdb439cf9e720523e66b6d20125d346ffe8fca")
    version("1.1.1", sha256="907c374d9c53b21b9f67ce648e7b2b09c320db234a1013d3f05919cd93c95a4b")
    version("1.1.0", sha256="b0c4ebe4988abc2b3434e6c50e7eb0612f3f401bc1aa79ad58a6a92dc87fa65b")
    version("1.0.0", sha256="a0eb269b84d7525b223dc650de12170bba30fbb3ae4f93eb2b5cbdce335e4da1")
    version("develop", branch="develop")
    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, when="@:1.5.5", description="Build with OpenMP support")
    variant("static", default=False, description="Build as static library")
    variant("cuda", default=False, description="CUDA backend")
    variant("rocm", default=False, description="ROCm backend")
    variant("fortran", default=False, description="Build fortran module")

    conflicts("+cuda", when="+rocm", msg="+cuda and +rocm are mutually exclusive")
    conflicts(
        "%gcc@13.0:",
        when="@1.5.0:1.5.4",
        msg="Version 1.5.0 to 1.5.4 is not compatible with GCC 13 and later.",
    )

    depends_on("mpi")
    depends_on("blas")
    depends_on("cmake@3.10:", type="build")
    depends_on("cmake@3.18:", type="build", when="@1.6.0:")

    depends_on("cuda", when="+cuda")
    depends_on("cuda@11:", when="@1.6.0: +cuda")

    depends_on("hip", when="+rocm")
    depends_on("rocblas", when="+rocm")
    conflicts("^rocblas@6.0.0:", when="@:1.5.5 +rocm")
    conflicts("^hip@6.0.0:", when="@:1.6.0 +rocm")  # v1.6.1 includes fix for hip 6.0

    # Propagate openmp to blas
    depends_on("openblas threads=openmp", when="+openmp ^[virtuals=blas] openblas")
    depends_on("amdblis threads=openmp", when="+openmp ^[virtuals=blas] amdblis")
    depends_on("blis threads=openmp", when="+openmp ^[virtuals=blas] blis")
    depends_on("intel-mkl threads=openmp", when="+openmp ^[virtuals=blas] intel-mkl")

    # Fix CMake find module for AMD BLIS,
    # which uses a different library name for the multi-threaded version
    patch("0001-amd_blis.patch", when="@1.3.0:1.4.0 ^amdblis")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("SPLA_FORTRAN", "fortran"),
            self.define_from_variant("SPLA_STATIC", "static"),
        ]

        if "+cuda" in spec:
            args += ["-DSPLA_GPU_BACKEND=CUDA"]
        elif "+rocm" in spec:
            args += ["-DSPLA_GPU_BACKEND=ROCM"]
        else:
            args += ["-DSPLA_GPU_BACKEND=OFF"]

        # v1.6.0: No longer has custom BLAS detection and only uses the FindBLAS CMake module.
        if spec.satisfies("@:1.5.5"):
            args += [self.define_from_variant("SPLA_OMP", "openmp")]
            if spec["blas"].name == "openblas":
                args += ["-DSPLA_HOST_BLAS=OPENBLAS"]
            elif spec["blas"].name in ["amdblis", "blis"]:
                args += ["-DSPLA_HOST_BLAS=BLIS"]
            elif spec["blas"].name == "atlas":
                args += ["-DSPLA_HOST_BLAS=ATLAS"]
            elif spec["blas"].name == "intel-mkl":
                args += ["-DSPLA_HOST_BLAS=MKL"]
            elif spec["blas"].name == "netlib-lapack":
                args += ["-DSPLA_HOST_BLAS=GENERIC"]
            elif spec["blas"].name == "cray-libsci":
                args += ["-DSPLA_HOST_BLAS=CRAY_LIBSCI"]
        else:
            args += [self.define("BLAS_LIBRARIES", spec["blas"].libs.joined(";"))]

        return args
