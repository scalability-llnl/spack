# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

# This limits the versions of lots of things pretty severely.
#
#   - Only v1.5.2 and newer are buildable.
#   - CMake must be v3.22 or newer.
#   - CUDA must be v11.0.0 or newer.


class Hydrogen(CachedCMakePackage, CudaPackage, ROCmPackage):
    """Hydrogen: Distributed-memory dense and sparse-direct linear algebra
    and optimization library. Based on the Elemental library."""

    homepage = "https://libelemental.org"
    url = "https://github.com/LLNL/Elemental/archive/v1.5.1.tar.gz"
    git = "https://github.com/LLNL/Elemental.git"
    tags = ["ecp", "radiuss"]

    maintainers("bvanessen")

    license("GPL-2.0-or-later")

    version("develop", branch="hydrogen")
    version("1.5.3", sha256="faefbe738bd364d0e26ce9ad079a11c93a18c6f075719a365fd4fa5f1f7a989a")
    version("1.5.2", sha256="a902cad3962471216cfa278ba0561c18751d415cd4d6b2417c02a43b0ab2ea33")
    version("1.5.1", sha256="447da564278f98366906d561d9c8bc4d31678c56d761679c2ff3e59ee7a2895c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    # Older versions are no longer supported.

    variant("shared", default=True, description="Enables the build of shared libraries.")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant("int64", default=False, description="Use 64-bit integers")
    variant("al", default=True, sticky=True, description="Use Aluminum communication library")
    variant(
        "cub", default=True, when="+cuda", description="Use CUB/hipCUB for GPU memory management"
    )
    variant(
        "cub", default=True, when="+rocm", description="Use CUB/hipCUB for GPU memory management"
    )
    variant("half", default=False, description="Support for FP16 precision data types")

    # TODO: Add netlib-lapack. For GPU-enabled builds, typical
    # workflows don't touch host BLAS/LAPACK all that often, and even
    # less frequently in performance-critical regions.
    variant(
        "blas",
        default="any",
        values=("any", "openblas", "mkl", "accelerate", "essl", "libsci"),
        description="Specify a host BLAS library preference",
    )
    variant("int64_blas", default=False, description="Use 64-bit integers for (host) BLAS.")

    variant("openmp", default=True, description="Make use of OpenMP within CPU kernels")
    variant(
        "omp_taskloops",
        when="+openmp",
        default=False,
        description="Use OpenMP taskloops instead of parallel for loops",
    )

    # Users should spec this on their own on the command line, no?
    # This doesn't affect Hydrogen itself at all. Not one bit.
    # variant(
    #     "openmp_blas",
    #     default=False,
    #     description="Use OpenMP for threading in the BLAS library")

    variant("test", default=False, description="Builds test suite")

    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("+half", when="+rocm", msg="FP16 support not implemented for ROCm.")

    depends_on("cmake@3.22.0:", type="build", when="@1.5.2:")
    depends_on("cmake@3.17.0:", type="build", when="@1.5.1")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    # Note that #1712 forces us to enumerate the different blas variants
    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on("openblas", when="blas=openblas")
    depends_on("openblas +ilp64", when="blas=openblas +int64_blas")
    depends_on("openblas@0.3.21:0.3.23", when="blas=openblas arch=ppc64le:")

    depends_on("intel-mkl", when="blas=mkl")
    depends_on("intel-mkl +ilp64", when="blas=mkl +int64_blas")

    # I don't think this is true...
    depends_on("veclibfort", when="blas=accelerate")

    depends_on("essl", when="blas=essl")
    depends_on("essl +ilp64", when="blas=essl +int64_blas")

    depends_on("netlib-lapack +external-blas", when="blas=essl")

    depends_on("cray-libsci", when="blas=libsci")

    # Specify the correct version of Aluminum
    depends_on("aluminum@0.7.0:", when="@1.5.2: +al")

    # Add Aluminum variants
    depends_on("aluminum +cuda +ht", when="+al +cuda")
    depends_on("aluminum +rocm +ht", when="+al +rocm")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("aluminum +cuda cuda_arch=%s" % arch, when="+al +cuda cuda_arch=%s" % arch)

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    for val in ROCmPackage.amdgpu_targets:
        depends_on(
            "aluminum +rocm amdgpu_target=%s" % val, when="+al +rocm amdgpu_target=%s" % val
        )

    depends_on("cuda@11.0.0:", when="+cuda")
    depends_on("hipcub +rocm", when="+rocm +cub")
    depends_on("half", when="+half")

    depends_on("llvm-openmp", when="%apple-clang +openmp")

    # Fixes https://github.com/spack/spack/issues/42286
    # https://github.com/LLNL/Elemental/pull/177
    patch("cmake-intel-mpi-escape-quotes-pr177.patch", when="@1.5.3")

    @property
    def libs(self):
        shared = True if self.spec.satisfies("+shared") else False
        return find_libraries("libHydrogen", root=self.prefix, shared=shared, recursive=True)

    def cmake_args(self):
        args = []
        return args

    def get_cuda_flags(self):
        spec = self.spec
        args = []
        if spec.satisfies("^cuda+allow-unsupported-compilers"):
            args.append("-allow-unsupported-compiler")

        if spec.satisfies("%clang"):
            for flag in spec.compiler_flags["cxxflags"]:
                if "gcc-toolchain" in flag:
                    args.append("-Xcompiler={0}".format(flag))
        return args

    def std_initconfig_entries(self):
        entries = super(Hydrogen, self).std_initconfig_entries()

        # CMAKE_PREFIX_PATH, in CMake types, is a "STRING", not a "PATH". :/
        entries = [x for x in entries if "CMAKE_PREFIX_PATH" not in x]
        cmake_prefix_path = os.environ["CMAKE_PREFIX_PATH"].replace(":", ";")
        entries.append(cmake_cache_string("CMAKE_PREFIX_PATH", cmake_prefix_path))
        # IDK why this is here, but it was in the original recipe. So, yeah.
        entries.append(cmake_cache_string("CMAKE_INSTALL_MESSAGE", "LAZY"))
        return entries

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super(Hydrogen, self).initconfig_compiler_entries()

        # FIXME: Enforce this better in the actual CMake.
        entries.append(cmake_cache_string("CMAKE_CXX_STANDARD", "17"))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", spec.satisfies("+shared")))
        entries.append(cmake_cache_option("CMAKE_EXPORT_COMPILE_COMMANDS", True))

        entries.append(cmake_cache_option("MPI_ASSUME_NO_BUILTIN_MPI", True))

        if spec.satisfies("%clang +openmp platform=darwin") or spec.satisfies(
            "%clang +omp_taskloops platform=darwin"
        ):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            entries.append(cmake_cache_string("OpenMP_CXX_FLAGS", "-fopenmp=libomp"))
            entries.append(cmake_cache_string("OpenMP_CXX_LIB_NAMES", "libomp"))
            entries.append(
                cmake_cache_string(
                    "OpenMP_libomp_LIBRARY", "{0}/lib/libomp.dylib".format(clang_root)
                )
            )

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super(Hydrogen, self).initconfig_hardware_entries()

        entries.append(cmake_cache_option("Hydrogen_ENABLE_CUDA", spec.satisfies("+cuda")))
        if spec.satisfies("+cuda"):
            entries.append(cmake_cache_string("CMAKE_CUDA_STANDARD", "17"))
            if not spec.satisfies("cuda_arch=none"):
                archs = spec.variants["cuda_arch"].value
                arch_str = ";".join(archs)
                entries.append(cmake_cache_string("CMAKE_CUDA_ARCHITECTURES", arch_str))

            # FIXME: Should this use the "cuda_flags" function of the
            # CudaPackage class or something? There might be other
            # flags in play, and we need to be sure to get them all.
            cuda_flags = self.get_cuda_flags()
            if len(cuda_flags) > 0:
                entries.append(cmake_cache_string("CMAKE_CUDA_FLAGS", " ".join(cuda_flags)))

        entries.append(cmake_cache_option("Hydrogen_ENABLE_ROCM", spec.satisfies("+rocm")))
        if spec.satisfies("+rocm"):
            entries.append(cmake_cache_string("CMAKE_HIP_STANDARD", "17"))
            if not spec.satisfies("amdgpu_target=none"):
                archs = self.spec.variants["amdgpu_target"].value
                arch_str = ";".join(archs)
                entries.append(cmake_cache_string("CMAKE_HIP_ARCHITECTURES", arch_str))
                entries.append(cmake_cache_string("AMDGPU_TARGETS", arch_str))
                entries.append(cmake_cache_string("GPU_TARGETS", arch_str))
            entries.append(cmake_cache_path("HIP_ROOT_DIR", spec["hip"].prefix))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = super(Hydrogen, self).initconfig_package_entries()

        # Basic Hydrogen options
        entries.append(cmake_cache_option("Hydrogen_ENABLE_TESTING", spec.satisfies("+test")))
        entries.append(cmake_cache_option("Hydrogen_GENERAL_LAPACK_FALLBACK", True))
        entries.append(cmake_cache_option("Hydrogen_USE_64BIT_INTS", spec.satisfies("+int64")))
        entries.append(
            cmake_cache_option("Hydrogen_USE_64BIT_BLAS_INTS", spec.satisfies("+int64_blas"))
        )

        # Advanced dependency options
        entries.append(cmake_cache_option("Hydrogen_ENABLE_ALUMINUM", spec.satisfies("+al")))
        entries.append(cmake_cache_option("Hydrogen_ENABLE_CUB", spec.satisfies("+cub")))
        entries.append(
            cmake_cache_option("Hydrogen_ENABLE_GPU_FP16", spec.satisfies("+cuda +half"))
        )
        entries.append(cmake_cache_option("Hydrogen_ENABLE_HALF", spec.satisfies("+half")))
        entries.append(cmake_cache_option("Hydrogen_ENABLE_OPENMP", spec.satisfies("+openmp")))
        entries.append(
            cmake_cache_option("Hydrogen_ENABLE_OMP_TASKLOOP", spec.satisfies("+omp_taskloops"))
        )

        # Note that CUDA/ROCm are handled above.

        if spec.satisfies("blas=openblas"):
            entries.append(
                cmake_cache_option("Hydrogen_USE_OpenBLAS", spec.satisfies("blas=openblas"))
            )
            # CMAKE_PREFIX_PATH should handle this
            entries.append(cmake_cache_string("OpenBLAS_DIR", spec["openblas"].prefix))
        elif spec.satisfies("blas=mkl") or spec.satisfies("^intel-mkl"):
            entries.append(cmake_cache_option("Hydrogen_USE_MKL", True))
        elif spec.satisfies("blas=essl") or spec.satisfies("^essl"):
            entries.append(cmake_cache_string("BLA_VENDOR", "IBMESSL"))
            # IF IBM ESSL is used it needs help finding the proper LAPACK libraries
            entries.append(
                cmake_cache_string(
                    "LAPACK_LIBRARIES",
                    "%s;-llapack;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                )
            )
            entries.append(
                cmake_cache_string(
                    "BLAS_LIBRARIES",
                    "%s;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                )
            )
        elif spec.satisfies("blas=accelerate"):
            entries.append(cmake_cache_option("Hydrogen_USE_ACCELERATE", True))
        elif spec.satisfies("^netlib-lapack"):
            entries.append(cmake_cache_string("BLA_VENDOR", "Generic"))

        return entries

    def setup_build_environment(self, env):
        if self.spec.satisfies("%apple-clang +openmp"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)
