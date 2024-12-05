# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cosma(CMakePackage):
    """
    Distributed Communication-Optimal Matrix-Matrix Multiplication Library
    """

    maintainers("haampie", "kabicm", "teonnik", "simonpintarelli", "mtaillefumier")
    homepage = "https://github.com/eth-cscs/COSMA"
    url = "https://github.com/eth-cscs/COSMA/archive/refs/tags/v2.6.6.tar.gz"
    git = "https://github.com/eth-cscs/COSMA.git"

    license("BSD-3-Clause")

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version("master", branch="master", submodules=False)
    version("2.6.6", sha256="1604be101e77192fbcc5551236bc87888d336e402f5409bbdd9dea900401cc37")
    version("2.6.5", sha256="10d9b7ecc1ce44ec5b9e0c0bf89278a63029912ec3ea99661be8576b553ececf")
    version("2.6.4", sha256="6d7bd5e3005874af9542a329c93e7ccd29ca1a5573dae27618fac2704fa2b6ab")
    version("2.6.3", sha256="c2a3735ea8f860930bea6706d968497d72a1be0498c689b5bc4a951ffc2d1146")
    version("2.6.2", sha256="2debb5123cc35aeebc5fd2f8a46cfd6356d1e27618c9bb57129ecd09aa400940")
    version("2.6.1", sha256="69aa6634a030674f0d9be61e7b0bf0dc17acf0fc9e7a90b40e3179e2254c8d67")
    version("2.5.1", sha256="085b7787597374244bbb1eb89bc69bf58c35f6c85be805e881e1c0b25166c3ce")
    version("2.5.0", sha256="7f68bb0ee5c80f9b8df858afcbd017ad4ed87ac09439d13d7d890844dbdd3d54")
    version("2.4.0", sha256="5714315ce06d48037f86cfee2d7f19340643fee95e9d7f1e92dc1b623b67e395")
    version("2.3.0", sha256="0c01c2deb5a0cd177952178350188a62c42ce55e604d7948ac472f55bf0d4815")
    version("2.2.0", sha256="1eb92a98110df595070a12193b9221eecf9d103ced8836c960f6c79a2bd553ca")
    version("2.0.7", sha256="8d70bfcbda6239b6a8fbeaca138790bbe58c0c3aa576879480d2632d4936cf7e")
    version("2.0.2", sha256="4f3354828bc718f3eef2f0098c3bdca3499297497a220da32db1acd57920c68d")

    depends_on("cxx", type="build")  # generated

    # We just need the libraries of cuda and rocm, so no need to extend
    # CudaPackage or ROCmPackage.
    variant("cuda", default=False, description="Build with cuBLAS support")
    variant("rocm", default=False, description="Build with rocBLAS support")
    variant("scalapack", default=False, description="Build with ScaLAPACK API")
    variant("shared", default=True, description="Build the shared library version")
    variant("tests", default=False, description="Build tests")
    variant("apps", default=False, description="Build miniapp")
    variant("profiling", default=False, description="Enable profiling")
    variant("gpu_direct", default=False, description="GPU aware MPI")

    with when("+cuda"):
        variant("nccl", default=False, description="Use cuda nccl")

    with when("+rocm"):
        variant("rccl", default=False, description="Use rocm rccl")

    depends_on("cmake@3.22:", type="build")
    depends_on("mpi@3:")
    depends_on("blas", when="~cuda ~rocm")
    depends_on("scalapack", when="+scalapack")
    depends_on("cuda", when="+cuda")
    depends_on("rocblas", when="+rocm")
    depends_on("nccl", when="+nccl")
    depends_on("rccl", when="+rccl")

    with when("@2.6.3:"):
        depends_on("tiled-mm@2.2:+cuda", when="+cuda")
        depends_on("tiled-mm@2.2:+rocm", when="+rocm")

    with when("@2.6.1:2.6.2"):
        depends_on("tiled-mm@2.0+rocm", when="+rocm")
        depends_on("tiled-mm@2.0+cuda", when="+cuda")

    with when("@2.6.1:"):
        depends_on("costa")
        depends_on("costa+scalapack", when="+scalapack")
        depends_on("cxxopts", when="+apps")
        depends_on("cxxopts", when="+tests")
        depends_on("semiprof", when="+profiling")
        depends_on("costa+profiling", when="+profiling")

    patch("fj-ssl2.patch", when="^fujitsu-ssl2")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+cuda"):
            env.set("CUDA_PATH", self.spec["cuda"].prefix)

    def cosma_blas_cmake_arg(self):
        query_to_cmake_arg = [
            ("+cuda", "CUDA"),
            ("+rocm", "ROCM"),
            ("^intel-mkl", "MKL"),
            ("^intel-oneapi-mkl", "MKL"),
            ("^cray-libsci", "CRAY_LIBSCI"),
            ("^netlib-lapack", "CUSTOM"),
            ("^openblas", "OPENBLAS"),
            ("^fujitsu-ssl2", "SSL2"),
        ]

        if self.version >= Version("2.4.0"):
            query_to_cmake_arg.extend(
                [("^blis", "BLIS"), ("^amdblis", "BLIS"), ("^atlas", "ATLAS")]
            )

        for query, cmake_arg in query_to_cmake_arg:
            if query in self.spec:
                return cmake_arg

        return "CUSTOM"

    def cosma_scalapack_cmake_arg(self):
        spec = self.spec

        if spec.satisfies("~scalapack"):
            return "OFF"
        elif spec.satisfies("^intel-mkl") or spec.satisfies("^intel-oneapi-mkl"):
            return "MKL"
        elif spec.satisfies("^cray-libsci"):
            return "CRAY_LIBSCI"

        return "CUSTOM"

    def cmake_args(self):
        return [
            self.define_from_variant("COSMA_WITH_TESTS", "tests"),
            self.define_from_variant("COSMA_WITH_APPS", "apps"),
            self.define_from_variant("COSMA_WITH_NCCL", "nccl"),
            self.define_from_variant("COSMA_WITH_RCCL", "rccl"),
            self.define_from_variant("COSMA_WITH_GPU_AWARE_MPI", "gpu_direct"),
            self.define_from_variant("COSMA_WITH_PROFILING", "profiling"),
            self.define("COSMA_WITH_BENCHMARKS", False),
            self.define("COSMA_BLAS", self.cosma_blas_cmake_arg()),
            self.define("COSMA_SCALAPACK", self.cosma_scalapack_cmake_arg()),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
