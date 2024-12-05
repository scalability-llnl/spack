# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.platforms.cray
from spack.package import *


class Aluminum(CachedCMakePackage, CudaPackage, ROCmPackage):
    """Aluminum provides a generic interface to high-performance
    communication libraries, with a focus on allreduce
    algorithms. Blocking and non-blocking algorithms and GPU-aware
    algorithms are supported. Aluminum also contains custom
    implementations of select algorithms to optimize for certain
    situations."""

    homepage = "https://github.com/LLNL/Aluminum"
    url = "https://github.com/LLNL/Aluminum/archive/v1.0.0.tar.gz"
    git = "https://github.com/LLNL/Aluminum.git"
    tags = ["ecp", "radiuss"]

    maintainers("benson31", "bvanessen")

    license("Apache-2.0")

    version("master", branch="master")
    version("1.4.1", sha256="d130a67fef1cb7a9cb3bbec1d0de426f020fe68c9df6e172c83ba42281cd90e3")
    version("1.4.0", sha256="ac54de058f38cead895ec8163f7b1fa7674e4dc5aacba683a660a61babbfe0c6")
    version("1.3.1", sha256="28ce0af6c6f29f97b7f19c5e45184bd2f8a0b1428f1e898b027d96d47cb74b0b")
    version("1.3.0", sha256="d0442efbebfdfb89eec793ae65eceb8f1ba65afa9f2e48df009f81985a4c27e3")
    version("1.2.3", sha256="9b214bdf30f9b7e8e017f83e6615db6be2631f5be3dd186205dbe3aa62f4018a")

    depends_on("cxx", type="build")  # generated

    # Library capabilities
    variant(
        "cuda_rma",
        default=False,
        when="+cuda",
        description="Builds with support for CUDA intra-node "
        " Put/Get and IPC RMA functionality",
    )
    variant(
        "ht",
        default=False,
        description="Builds with support for host-enabled MPI"
        " communication of accelerator data",
    )
    variant("nccl", default=False, description="Builds with support for NCCL communication lib")
    variant("shared", default=True, description="Build Aluminum as a shared library")

    # Debugging features
    variant("hang_check", default=False, description="Enable hang checking")
    variant("trace", default=False, description="Enable runtime tracing")

    # Profiler support
    variant("nvtx", default=False, when="+cuda", description="Enable profiling via nvprof/NVTX")
    variant(
        "roctracer", default=False, when="+rocm", description="Enable profiling via rocprof/roctx"
    )

    # Advanced options
    variant("mpi_serialize", default=False, description="Serialize MPI operations")
    variant("stream_mem_ops", default=False, description="Enable stream memory operations")
    variant(
        "thread_multiple",
        default=False,
        description="Allow multiple threads to call Aluminum concurrently",
    )

    # Benchmark/testing support
    variant(
        "benchmarks",
        default=False,
        description="Build the Aluminum benchmarking drivers "
        "(warning: may significantly increase build time!)",
    )
    variant(
        "tests",
        default=False,
        description="Build the Aluminum test drivers "
        "(warning: may moderately increase build time!)",
    )

    # FIXME: Do we want to expose tuning parameters to the Spack
    # recipe? Some are numeric values, some are on/off switches.

    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm support are mutually exclusive")

    depends_on("mpi")

    depends_on("cmake@3.21.0:", type="build", when="@1.0.1:")
    depends_on("hwloc@1.11:")

    with when("+cuda"):
        depends_on("cub", when="^cuda@:10")
        depends_on("hwloc +cuda +nvml")
        with when("+nccl"):
            depends_on("nccl@2.7.0-0:")
            for arch in CudaPackage.cuda_arch_values:
                depends_on(
                    "nccl +cuda cuda_arch={0}".format(arch),
                    when="+cuda cuda_arch={0}".format(arch),
                )
            if spack.platforms.cray.slingshot_network():
                depends_on("aws-ofi-nccl")  # Note: NOT a CudaPackage

    with when("+rocm"):
        for val in ROCmPackage.amdgpu_targets:
            depends_on(
                "hipcub +rocm amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )
            depends_on(
                "hwloc@2.3.0: +rocm amdgpu_target={0}".format(val),
                when="amdgpu_target={0}".format(val),
            )
            # RCCL is *NOT* implented as a ROCmPackage
            depends_on(
                "rccl amdgpu_target={0}".format(val), when="+nccl amdgpu_target={0}".format(val)
            )
            depends_on(
                "roctracer-dev +rocm amdgpu_target={0}".format(val),
                when="+roctracer amdgpu_target={0}".format(val),
            )
        if spack.platforms.cray.slingshot_network():
            depends_on("aws-ofi-rccl", when="+nccl")

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
        entries = super(Aluminum, self).std_initconfig_entries()

        # CMAKE_PREFIX_PATH, in CMake types, is a "STRING", not a "PATH". :/
        entries = [x for x in entries if "CMAKE_PREFIX_PATH" not in x]
        cmake_prefix_path = os.environ["CMAKE_PREFIX_PATH"].replace(":", ";")
        entries.append(cmake_cache_string("CMAKE_PREFIX_PATH", cmake_prefix_path))
        return entries

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super(Aluminum, self).initconfig_compiler_entries()

        # FIXME: Enforce this better in the actual CMake.
        entries.append(cmake_cache_string("CMAKE_CXX_STANDARD", "17"))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", "+shared" in spec))
        entries.append(cmake_cache_option("CMAKE_EXPORT_COMPILE_COMMANDS", True))
        entries.append(cmake_cache_option("MPI_ASSUME_NO_BUILTIN_MPI", True))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super(Aluminum, self).initconfig_hardware_entries()

        entries.append(cmake_cache_option("ALUMINUM_ENABLE_CUDA", "+cuda" in spec))
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

        entries.append(cmake_cache_option("ALUMINUM_ENABLE_ROCM", "+rocm" in spec))
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
        entries = super(Aluminum, self).initconfig_package_entries()

        # Library capabilities
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_MPI_CUDA", "+cuda_rma" in spec))
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_MPI_CUDA_RMA", "+cuda_rma" in spec))
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_HOST_TRANSFER", "+ht" in spec))
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_NCCL", "+nccl" in spec))

        # Debugging features
        entries.append(cmake_cache_option("ALUMINUM_DEBUG_HANG_CHECK", "+hang_check" in spec))
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_TRACE", "+trace" in spec))

        # Profiler support
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_NVPROF", "+nvtx" in spec))
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_ROCTRACER", "+roctracer" in spec))

        # Advanced options
        entries.append(cmake_cache_option("ALUMINUM_MPI_SERIALIZE", "+mpi_serialize" in spec))
        entries.append(
            cmake_cache_option("ALUMINUM_ENABLE_STREAM_MEM_OPS", "+stream_mem_ops" in spec)
        )
        entries.append(
            cmake_cache_option("ALUMINUM_ENABLE_THREAD_MULTIPLE", "+thread_multiple" in spec)
        )

        # Benchmark/testing support
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_BENCHMARKS", "+benchmarks" in spec))
        entries.append(cmake_cache_option("ALUMINUM_ENABLE_TESTS", "+tests" in spec))

        return entries
