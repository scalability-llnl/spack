# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import socket

from spack.package import *

from .blt import llnl_link_helpers


class RajaPerf(CachedCMakePackage, CudaPackage, ROCmPackage):
    """RAJA Performance Suite."""

    homepage = "https://github.com/LLNL/RAJAPerf"
    git = "https://github.com/LLNL/RAJAPerf.git"
    tags = ["radiuss"]

    maintainers("davidbeckingsale", "adrienbernede")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules="True")
    version("main", branch="main", submodules="True")
    version(
        "2024.07.0",
        tag="v2024.07.0",
        commit="6e81aa58af244a13755a694bfdc7bc301139a244",
        submodules="True",
    )
    version(
        "2023.06.0",
        tag="v2023.06.0",
        commit="e5b2102f50e4642f53d9c86fb622b398a748974a",
        submodules="True",
    )
    version(
        "2022.10.0",
        tag="v2022.10.0",
        commit="57ee53e402d2ac0a398df39ad1ca85cf1d2be45b",
        submodules="True",
    )
    version(
        "0.12.0",
        tag="v0.12.0",
        commit="388c1d7562e1cb364191cb34c1ff62f3cadf54a0",
        submodules="True",
    )
    version(
        "0.11.0",
        tag="v0.11.0",
        commit="22ac1de533ebd477c781d53962a92478c0a11d43",
        submodules="True",
    )
    version(
        "0.10.0",
        tag="v0.10.0",
        commit="6bf725af38da41b1ebd1d29c75ffa5b8e57f7cbf",
        submodules="True",
    )
    version(
        "0.9.0", tag="v0.9.0", commit="064dd17dae696c3e440eeb7469fa90341858a636", submodules="True"
    )
    version(
        "0.8.0", tag="v0.8.0", commit="94c65b2caefec2220f712f34c2a198b682ca7e23", submodules="True"
    )
    version(
        "0.7.0", tag="v0.7.0", commit="a6ef0279d9d240199947d872d8f28bf121f2192c", submodules="True"
    )
    version(
        "0.6.0", tag="v0.6.0", commit="21e476f031bc10bbdb8514425c380553bfb23bdc", submodules="True"
    )
    version(
        "0.5.2", tag="v0.5.2", commit="2da5e27bc648ff5540ffa69bbde67f125e4581d3", submodules="True"
    )
    version(
        "0.5.1", tag="v0.5.1", commit="a7b6f63e4fef2d0146932eff409788da51ab0cb3", submodules="True"
    )
    version(
        "0.5.0", tag="v0.5.0", commit="888f5ebe69a9b2ae35058cf8fb8d89d91a379bea", submodules="True"
    )
    version(
        "0.4.0", tag="v0.4.0", commit="a8f669c1ad01d51132a4e3d9d6aa8b2cabc9eff0", submodules="True"
    )

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI support")
    variant("openmp", default=False, description="Build OpenMP backend")
    variant("omptarget", default=False, description="Build with OpenMP target support")
    variant("sycl", default=False, description="Build sycl backend")
    variant("shared", default=False, description="Build Shared Libs")
    variant("omptask", default=False, description="Build OpenMP task variants of algorithms")
    variant(
        "tests",
        default="basic",
        values=("none", "basic", "benchmarks"),
        multi=False,
        description="Tests to run",
    )
    variant("caliper", default=False, description="Build with support for Caliper based profiling")

    depends_on("blt")
    depends_on("blt@0.6.2:", type="build", when="@2024.07.0:")
    depends_on("blt@0.5.3", type="build", when="@2023.06")
    depends_on("blt@0.5.2:0.5.3", type="build", when="@2022.10")
    depends_on("blt@0.5.0:", type="build", when="@0.12.0:")
    depends_on("blt@0.4.1:", type="build", when="@0.11.0:")
    depends_on("blt@0.4.0:", type="build", when="@0.8.0:")
    depends_on("blt@0.3.0:", type="build", when="@:0.7.0")

    depends_on("cmake@3.23:", when="@2024.07.0:", type="build")
    depends_on("cmake@3.23:", when="@0.12.0:2023.06.0 +rocm", type="build")
    depends_on("cmake@3.20:", when="@0.12.0:2023.06.0", type="build")
    depends_on("cmake@3.14:", when="@:0.12.0", type="build")

    depends_on("mpi", when="+mpi")

    depends_on("llvm-openmp", when="+openmp %apple-clang")

    depends_on("rocprim", when="+rocm")

    depends_on("caliper@2.9.0:", when="+caliper")
    depends_on("caliper@2.9.0: +cuda", when="+caliper +cuda")
    depends_on("caliper@2.9.0: +rocm", when="+caliper +rocm")

    with when("@0.12.0: +rocm +caliper"):
        depends_on("caliper +rocm")
        for arch in ROCmPackage.amdgpu_targets:
            depends_on(
                "caliper +rocm amdgpu_target={0}".format(arch),
                when="amdgpu_target={0}".format(arch),
            )
        conflicts("+openmp", when="@:2022.03")

    with when("@0.12.0: +cuda +caliper"):
        depends_on("caliper +cuda")
        for sm_ in CudaPackage.cuda_arch_values:
            depends_on("caliper +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))

    conflicts("~openmp", when="+omptarget", msg="OpenMP target requires OpenMP")
    conflicts("+cuda", when="+omptarget", msg="Cuda may not be activated when omptarget is ON")
    conflicts("+omptarget +rocm")
    conflicts("+sycl +omptarget")
    conflicts("+sycl +rocm")
    # Using RAJA version as threshold on purpose (no 2024.02 version of RAJAPerf were released).
    conflicts(
        "+sycl",
        when="@:2024.02.99",
        msg="Support for SYCL was introduced in RAJA after 2024.02 release, "
        "please use a newer release.",
    )

    def _get_sys_type(self, spec):
        sys_type = str(spec.architecture)
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            hostname = hostname.rstrip("1234567890")
        return "{0}-{1}-{2}@{3}-{4}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
            self.spec.dag_hash(8),
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        compiler = self.compiler
        # Default entries are already defined in CachedCMakePackage, inherit them:
        entries = super().initconfig_compiler_entries()

        if spec.satisfies("+rocm"):
            entries.insert(0, cmake_cache_path("CMAKE_CXX_COMPILER", spec["hip"].hipcc))

        # adrienbernede-23-01
        # Maybe we want to share this in the above llnl_link_helpers function.
        compilers_using_cxx14 = ["intel-17", "intel-18", "xl"]
        if any(compiler in self.compiler.cxx for compiler in compilers_using_cxx14):
            entries.append(cmake_cache_string("BLT_CXX_STD", "c++14"))

        llnl_link_helpers(entries, spec, compiler)

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        compiler = self.compiler
        entries = super().initconfig_hardware_entries()

        entries.append("#------------------{0}".format("-" * 30))
        entries.append("# Package custom hardware settings")
        entries.append("#------------------{0}\n".format("-" * 30))

        entries.append(cmake_cache_option("ENABLE_OPENMP", "+openmp" in spec))

        # T benefit from the shared function "cuda_for_radiuss_projects",
        # we do not modify CMAKE_CUDA_FLAGS: it is already appended by the
        # shared function.
        if "+cuda" in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))
            # Shared handling of cuda.

            # Custom options.
            # We place everything in CMAKE_CUDA_FLAGS_(RELEASE|RELWITHDEBINFO|DEBUG)
            # which are not set by cuda_for_radiuss_projects
            if "xl" in compiler.cxx:
                all_targets_flags = (
                    "-Xcompiler -qstrict -Xcompiler -qxlcompatmacros -Xcompiler -qalias=noansi"
                    + "-Xcompiler -qsmp=omp -Xcompiler -qhot -Xcompiler -qnoeh"
                    + "-Xcompiler -qsuppress=1500-029 -Xcompiler -qsuppress=1500-036"
                    + "-Xcompiler -qsuppress=1500-030"
                )
                cuda_release_flags = "-O3 -Xcompiler -O2 " + all_targets_flags
                cuda_reldebinf_flags = "-O3 -g -Xcompiler -O2 " + all_targets_flags
                cuda_debug_flags = "-O0 -g -Xcompiler -O2 " + all_targets_flags

            elif "gcc" in compiler.cxx:
                all_targets_flags = "-Xcompiler -finline-functions -Xcompiler -finline-limit=20000"

                cuda_release_flags = "-O3 -Xcompiler -Ofast " + all_targets_flags
                cuda_reldebinf_flags = "-O3 -g -Xcompiler -Ofast " + all_targets_flags
                cuda_debug_flags = "-O0 -g -Xcompiler -O0 " + all_targets_flags

            else:
                all_targets_flags = "-Xcompiler -finline-functions"

                cuda_release_flags = "-O3 -Xcompiler -Ofast " + all_targets_flags
                cuda_reldebinf_flags = "-O3 -g -Xcompiler -Ofast " + all_targets_flags
                cuda_debug_flags = "-O0 -g -Xcompiler -O0 " + all_targets_flags

            entries.append(cmake_cache_string("CMAKE_CUDA_FLAGS_RELEASE", cuda_release_flags))
            entries.append(
                cmake_cache_string("CMAKE_CUDA_FLAGS_RELWITHDEBINFO", cuda_reldebinf_flags)
            )
            entries.append(cmake_cache_string("CMAKE_CUDA_FLAGS_DEBUG", cuda_debug_flags))

        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if "+rocm" in spec:
            entries.append(cmake_cache_option("ENABLE_HIP", True))
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

        entries.append(cmake_cache_option("ENABLE_OPENMP_TARGET", "+omptarget" in spec))
        if "+omptarget" in spec:
            if "%xl" in spec:
                entries.append(
                    cmake_cache_string(
                        "BLT_OPENMP_COMPILE_FLAGS", "-qoffload;-qsmp=omp;-qnoeh;-qalias=noansi"
                    )
                )
                entries.append(
                    cmake_cache_string(
                        "BLT_OPENMP_LINK_FLAGS", "-qoffload;-qsmp=omp;-qnoeh;-qalias=noansi"
                    )
                )
            if "%clang" in spec:
                entries.append(
                    cmake_cache_string(
                        "BLT_OPENMP_COMPILE_FLAGS", "-fopenmp;-fopenmp-targets=nvptx64-nvidia-cuda"
                    )
                )
                entries.append(
                    cmake_cache_string(
                        "BLT_OPENMP_LINK_FLAGS", "-fopenmp;-fopenmp-targets=nvptx64-nvidia-cuda"
                    )
                )

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec
        entries = super().initconfig_mpi_entries()

        entries.append(cmake_cache_option("ENABLE_MPI", "+mpi" in spec))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        # option_prefix = "RAJA_" if spec.satisfies("@0.14.0:") else ""

        # TPL locations
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# TPLs")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec["blt"].prefix))
        if "caliper" in self.spec:
            entries.append(
                cmake_cache_path("caliper_DIR", spec["caliper"].prefix + "/share/cmake/caliper/")
            )
            entries.append(
                cmake_cache_path("adiak_DIR", spec["adiak"].prefix + "/lib/cmake/adiak/")
            )

        # Build options
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# Build Options")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_string("CMAKE_BUILD_TYPE", spec.variants["build_type"].value))

        entries.append(cmake_cache_string("RAJA_RANGE_ALIGN", "4"))
        entries.append(cmake_cache_string("RAJA_RANGE_MIN_LENGTH", "32"))
        entries.append(cmake_cache_string("RAJA_DATA_ALIGN", "64"))

        entries.append(cmake_cache_option("RAJA_HOST_CONFIG_LOADED", True))

        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", "+shared" in spec))
        entries.append(cmake_cache_option("ENABLE_OPENMP", "+openmp" in spec))
        entries.append(cmake_cache_option("RAJA_ENABLE_OPENMP_TASK", "+omptask" in spec))
        entries.append(cmake_cache_option("ENABLE_SYCL", spec.satisfies("+sycl")))

        # C++17
        if spec.satisfies("@2024.07.0:") and spec.satisfies("+sycl"):
            entries.append(cmake_cache_string("BLT_CXX_STD", "c++17"))
        # C++14
        # Using RAJA version as threshold on purpose (no 0.14 version of RAJAPerf were released).
        elif spec.satisfies("@0.14.0:"):
            entries.append(cmake_cache_string("BLT_CXX_STD", "c++14"))

        entries.append(cmake_cache_option("ENABLE_BENCHMARKS", "tests=benchmarks" in spec))
        entries.append(
            cmake_cache_option("ENABLE_TESTS", "tests=none" not in spec or self.run_tests)
        )

        entries.append(cmake_cache_option("RAJA_PERFSUITE_USE_CALIPER", "+caliper" in spec))

        return entries

    def cmake_args(self):
        return []
