# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

# Each LAPACK++ version requires a specific BLAS++ version
_versions = [
    # LAPACK++,     BLAS++
    ["master", "master"],
    ["2024.05.31", "2024.05.31"],
    ["2023.11.05", "2023.11.05"],
    ["2023.08.25", "2023.08.25"],
    ["2023.06.00", "2023.06.00"],
    ["2022.07.00", "2022.07.00"],
    ["2022.05.00", "2022.05.00"],
    ["2020.10.00", "2020.10.00"],
    ["2020.10.01", "2020.10.01"],
    ["2020.10.02", "2020.10.02"],
    ["2021.04.00", "2021.04.01:"],  # or later
]


class Lapackpp(CMakePackage, CudaPackage, ROCmPackage):
    """LAPACK++: C++ API for the LAPACK Linear Algebra Package. Developed
    by the Innovative Computing Laboratory at the University of Tennessee,
    Knoxville."""

    homepage = "https://github.com/icl-utk-edu/lapackpp"
    git = homepage
    url = "https://github.com/icl-utk-edu/lapackpp/releases/download/v2023.01.00/lapackpp-2023.01.00.tar.gz"
    maintainers("teonnik", "Sely85", "G-Ragghianti", "mgates3")

    license("BSD-3-Clause")

    version("master", branch="master")
    version(
        "2024.05.31", sha256="093646d492a4c2c6b4d7001effb559c80da7fa31fd5ba517a6d686ca8c78cd99"
    )
    version(
        "2023.11.05", sha256="9a505ef4e76504b6714cc19eb1b58939694f9ab51427a5bb915b016d615570ca"
    )
    version(
        "2023.08.25", sha256="9effdd616a4a183a9b37c2ad33c85ddd3d6071b183e8c35e02243fbaa7333d4d"
    )
    version(
        "2023.06.00", sha256="93df8392c859071120e00239feb96a0e060c0bb5176ee3a4f03eb9777c4edead"
    )
    version(
        "2022.07.00", sha256="11e59efcc7ea0764a2bfc0e0f7b1abf73cee2943c1df11a19601780641a9aa18"
    )
    version(
        "2022.05.00", sha256="d0f548cbc9d4ac46b1f961834d113173c0b433074f77bcfd69c7c31cb89b7ff2"
    )
    version(
        "2021.04.00", sha256="67abd8de9757dba86eb5d154cdb91f176b6c8b2b7d8e2a669ba0c221c4bb60ed"
    )
    version(
        "2020.10.02", sha256="8dde9b95d75b494c4f8b893d68034e95b7a7541981359acb97b6c1c4a9c45cd9"
    )
    version(
        "2020.10.01", sha256="ecd659730b4c3cfb8d2595f9bbb6af65d96b79397db654f17fe045bdfea841c0"
    )
    version(
        "2020.10.00", sha256="5f6ab3bd3794711818a3a50198efd29571520bf455e13ffa8ba50fa8376d7d1a"
    )

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared library")
    variant("sycl", default=False, description="Build support for the SYCL backend")

    # Match each LAPACK++ version to a specific BLAS++ version
    for lpp_ver, bpp_ver in _versions:
        depends_on("blaspp@" + bpp_ver, when="@" + lpp_ver)

    depends_on("blaspp ~cuda", when="~cuda")
    depends_on("blaspp +cuda", when="+cuda")
    depends_on("blaspp ~sycl", when="~sycl")
    depends_on("blaspp +sycl", when="+sycl")
    depends_on("blaspp ~rocm", when="~rocm")
    for val in ROCmPackage.amdgpu_targets:
        depends_on("blaspp +rocm amdgpu_target=%s" % val, when="amdgpu_target=%s" % val)

    depends_on("blas")
    depends_on("lapack")
    depends_on("rocblas", when="+rocm")
    depends_on("rocsolver", when="+rocm")
    depends_on("intel-oneapi-mkl threads=openmp", when="+sycl")

    backend_msg = "LAPACK++ supports only one GPU backend at a time"
    conflicts("+rocm", when="+cuda", msg=backend_msg)
    conflicts("+rocm", when="+sycl", msg=backend_msg)
    conflicts("+cuda", when="+sycl", msg=backend_msg)
    conflicts("+sycl", when="@:2023.06.00", msg="+sycl requires LAPACK++ version 2023.08.25")

    requires("%oneapi", when="+sycl", msg="lapackpp+sycl must be compiled with %oneapi")

    def cmake_args(self):
        spec = self.spec

        backend = "none"
        if self.version >= Version("2022.07.00"):
            if spec.satisfies("+cuda"):
                backend = "cuda"
            if spec.satisfies("+rocm"):
                backend = "hip"
            if spec.satisfies("+sycl"):
                backend = "sycl"

        args = [
            "-DBUILD_SHARED_LIBS=%s" % spec.satisfies("+shared"),
            "-Dbuild_tests=%s" % self.run_tests,
            "-DLAPACK_LIBRARIES=%s" % spec["lapack"].libs.joined(";"),
            "-Dgpu_backend=%s" % backend,
        ]

        if spec["blas"].name == "cray-libsci":
            args.append(self.define("BLA_VENDOR", "CRAY"))

        return args

    def check(self):
        # If the tester fails to build, ensure that the check() fails.
        if os.path.isfile(join_path(self.builder.build_directory, "test", "tester")):
            with working_dir(self.builder.build_directory):
                make("check")
        else:
            raise Exception("The tester was not built!")

    def flag_handler(self, name, flags):
        if (self.spec["blas"].name == "cray-libsci") and name == "cxxflags":
            flags.append("-DLAPACK_FORTRAN_ADD_")
        return (None, None, flags)
