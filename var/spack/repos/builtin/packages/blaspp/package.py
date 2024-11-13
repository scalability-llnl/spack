# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Blaspp(CMakePackage, CudaPackage, ROCmPackage):
    """C++ API for the Basic Linear Algebra Subroutines. Developed by the
    Innovative Computing Laboratory at the University of Tennessee,
    Knoxville."""

    homepage = "https://github.com/icl-utk-edu/blaspp"
    git = homepage
    url = "https://github.com/icl-utk-edu/blaspp/releases/download/v2023.01.00/blaspp-2023.01.00.tar.gz"
    maintainers("teonnik", "Sely85", "G-Ragghianti", "mgates3")

    license("BSD-3-Clause")

    version("master", branch="master")
    version(
        "2024.05.31", sha256="24f325d2e1c2cc4275324bd88406555688379480877d19553656a0328287927a"
    )
    version(
        "2023.11.05", sha256="62dfc03ec07c0826e0466dc2c204b460caa929d53ad4f050cb132d92670be7ce"
    )
    version(
        "2023.08.25", sha256="1d9c7227a6d8776944aa866592142b7b51c6e4ba5529d168eb8ae2b329c47401"
    )
    version(
        "2023.06.00", sha256="e261ad6cde2aa4f97e985aa9067f4c40d2aaa856904bb78007a3dcadf1378ae9"
    )
    version(
        "2022.07.00", sha256="566bd644f0364caffde6669e0f86514658eb06ca3d252a4fe67203921a875481"
    )
    version(
        "2022.05.00", sha256="696277859bc1bd9c0aeb0cb170a1e259765c0a86af49b20afa0ffcbabc3e207e"
    )
    version(
        "2021.04.01", sha256="11fc7b7e725086532ada58c0de53f30e480c2a06f1497b8081ea6d8f97e26150"
    )
    version(
        "2020.10.02", sha256="36e45bb5a8793ba5d7bc7c34fc263f91f92b0946634682937041221a6bf1a150"
    )
    version(
        "2020.10.01", sha256="1a05dbc46caf797d59a7c189216b876fdb1b2ff3e2eb48f1e6ca4b2756c59153"
    )
    version(
        "2020.10.00", sha256="ce148cfe397428d507c72d7d9eba5e9d3f55ad4cd842e6e873c670183dcb7795"
    )

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Use OpenMP internally.")
    variant("shared", default=True, description="Build shared libraries")
    variant("sycl", default=False, description="Build support for the SYCL backend")

    depends_on("cmake@3.15.0:", type="build")
    depends_on("blas")
    depends_on("llvm-openmp", when="%apple-clang +openmp")
    depends_on("rocblas", when="+rocm")
    depends_on("intel-oneapi-mkl", when="+sycl")
    depends_on("intel-oneapi-mkl threads=openmp", when="+sycl")

    # only supported with clingo solver: virtual dependency preferences
    # depends_on('openblas threads=openmp', when='+openmp ^openblas')

    # BLAS++ tests will fail when using openblas > 0.3.5 without multithreading support
    # locking is only supported in openblas 3.7+
    conflicts("^openblas@0.3.6 threads=none", msg="BLAS++ requires a threadsafe openblas")
    conflicts("^openblas@0.3.7: ~locking", msg="BLAS++ requires a threadsafe openblas")

    conflicts(
        "+rocm", when="@:2020.10.02", msg="ROCm support requires BLAS++ 2021.04.00 or greater"
    )
    backend_msg = "BLAS++ supports only one GPU backend at a time"
    conflicts("+rocm", when="+cuda", msg=backend_msg)
    conflicts("+rocm", when="+sycl", msg=backend_msg)
    conflicts("+cuda", when="+sycl", msg=backend_msg)
    conflicts("+sycl", when="@:2023.06.00", msg="SYCL support requires BLAS++ version 2023.08.25")

    requires("%oneapi", when="+sycl", msg="blaspp+sycl must be compiled with %oneapi")

    patch("0001-fix-blaspp-build-error-with-rocm-6.0.0.patch", when="@2023.06.00: ^hip@6.0 +rocm")

    def cmake_args(self):
        spec = self.spec
        backend_config = "-Duse_cuda=%s" % ("+cuda" in spec)
        if self.version >= Version("2021.04.01"):
            backend = "none"
            if spec.satisfies("+cuda"):
                backend = "cuda"
            if spec.satisfies("+rocm"):
                backend = "hip"
            if spec.satisfies("+sycl"):
                backend = "sycl"
            backend_config = "-Dgpu_backend=%s" % backend

        args = [
            "-Dbuild_tests=%s" % self.run_tests,
            "-Duse_openmp=%s" % ("+openmp" in spec),
            "-DBUILD_SHARED_LIBS=%s" % ("+shared" in spec),
            backend_config,
            "-DBLAS_LIBRARIES=%s" % spec["blas"].libs.joined(";"),
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
