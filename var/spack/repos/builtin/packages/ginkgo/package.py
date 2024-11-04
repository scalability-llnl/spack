# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Ginkgo(CMakePackage, CudaPackage, ROCmPackage):
    """High-performance linear algebra library for manycore systems,
    with a focus on sparse solution of linear systems."""

    homepage = "https://ginkgo-project.github.io/"
    git = "https://github.com/ginkgo-project/ginkgo.git"

    test_requires_compiler = True

    maintainers("MarcelKoch", "hartwiganzt")

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.8.0", commit="586b1754058d7a32d4bd1b650f9603484c2a8927")  # v1.8.0
    version("1.7.0", commit="49242ff89af1e695d7794f6d50ed9933024b66fe")  # v1.7.0
    version("1.6.0", commit="1f1ed46e724334626f016f105213c047e16bc1ae")  # v1.6.0
    version("1.5.0", commit="234594c92b58e2384dfb43c2d08e7f43e2b58e7a")  # v1.5.0
    version(
        "1.5.0.glu_experimental",
        branch="glu_experimental",
        commit="e234eab1bd7afe85dd594638e291a2caf464bfb1",
    )
    version("1.4.0", commit="f811917c1def4d0fcd8db3fe5c948ce13409e28e")  # v1.4.0
    version("1.3.0", commit="4678668c66f634169def81620a85c9a20b7cec78")  # v1.3.0
    version("1.2.0", commit="b4be2be961fd5db45c3d02b5e004d73550722e31")  # v1.2.0
    version("1.1.1", commit="08d2c5200d3c78015ac8a4fd488bafe1e4240cf5")  # v1.1.1
    version("1.1.0", commit="b9bec8225442b3eb2a85a870efa112ab767a17fb")  # v1.1.0
    version("1.0.0", commit="45244641e0c2b19ba33aecd25153c0bddbcbe1a0")  # v1.0.0

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("full_optimizations", default=False, description="Compile with all optimizations")
    variant("openmp", default=sys.platform != "darwin", description="Build with OpenMP")
    variant("sycl", default=False, description="Enable SYCL backend")
    variant("develtools", default=False, description="Compile with develtools enabled")
    variant("hwloc", default=False, description="Enable HWLOC support")
    variant("sde", default=False, description="Enable PAPI SDE support", when="@1.7.0:")
    variant("mpi", default=False, description="Enable MPI support", when="@1.5.0:")

    depends_on("cmake@3.9:", type="build", when="@:1.3.0")
    depends_on("cmake@3.13:", type="build", when="@1.4.0:1.6.0")
    depends_on("cmake@3.16:", type="build", when="@1.7.0:")
    depends_on("cmake@3.18:", type="build", when="+cuda@1.7.0:")
    depends_on("cmake@3.21:", type="build", when="+rocm@1.8.0:")
    depends_on("cuda@9:", when="+cuda @:1.4.0")
    depends_on("cuda@9.2:", when="+cuda @1.5.0:")
    depends_on("cuda@10.1:", when="+cuda @1.7.0:")
    depends_on("mpi@3.1:", when="+mpi")

    depends_on("rocthrust", when="+rocm")
    depends_on("hipsparse", when="+rocm")
    depends_on("hipblas", when="+rocm")
    depends_on("rocrand", when="+rocm")
    depends_on("hiprand", when="+rocm")
    depends_on("hipfft", when="+rocm")
    # ROCPRIM is not a direct dependency, but until we have reviewed our CMake
    # setup for rocthrust, this needs to also be added here.
    depends_on("rocprim", when="+rocm")
    depends_on("hwloc@2.1:", when="+hwloc")
    # TODO: replace with the next PAPI version when available (>7.0.1.0)
    depends_on("papi@master+sde", when="+sde")

    depends_on("googletest", type="test")
    depends_on("numactl", type="test", when="+hwloc")

    depends_on("intel-oneapi-mkl", when="+sycl")
    depends_on("intel-oneapi-dpl", when="+sycl")
    depends_on("intel-oneapi-tbb", when="+sycl")

    conflicts("%gcc@:5.2.9")
    conflicts("+rocm", when="@:1.1.1")

    # ROCm 4.1.0 breaks platform settings which breaks Ginkgo's HIP support.
    conflicts("^hip@4.1.0:", when="@:1.3.0")
    conflicts("^hipblas@4.1.0:", when="@:1.3.0")
    conflicts("^hipsparse@4.1.0:", when="@:1.3.0")
    conflicts("^rocthrust@4.1.0:", when="@:1.3.0")
    conflicts("^rocprim@4.1.0:", when="@:1.3.0")

    # Ginkgo 1.6.0 start relying on ROCm 4.5.0
    conflicts("^hip@:4.3.1", when="@1.6.0:")
    conflicts("^hipblas@:4.3.1", when="@1.6.0:")
    conflicts("^hipsparse@:4.3.1", when="@1.6.0:")
    conflicts("^rocthrust@:4.3.1", when="@1.6.0:")
    conflicts("^rocprim@:4.3.1", when="@1.6.0:")

    conflicts(
        "+sycl", when="@:1.4.0", msg="For SYCL support, please use Ginkgo version 1.4.0 and newer."
    )

    # Probably fixed in NVIDIA/cccl#1528 which hopefully comes with the next CUDA release
    conflicts("^cuda@12.4", when="+cuda", msg="CCCL 2.3 bug causes build failure.")

    # https://github.com/ginkgo-project/ginkgo/pull/1524
    patch("ginkgo-sycl-pr1524.patch", when="@1.7.0 +sycl %oneapi@2024:")

    # https://github.com/ginkgo-project/ginkgo/pull/1585
    patch("ginkgo-dpcpp-intrinsincs-oneapi-2024.1.patch", when="@1.7.0 +sycl %oneapi@2024.1:")

    # Skip smoke tests if compatible hardware isn't found
    patch("1.4.0_skip_invalid_smoke_tests.patch", when="@1.4.0")

    # Add missing include statement
    patch("thrust-count-header.patch", when="+rocm @1.5.0")

    # Correctly find rocthrust through CMake
    patch(
        "https://github.com/ginkgo-project/ginkgo/pull/1668.patch?full_index=1",
        sha256="27d6ae6c87bec15464d20a963c336e89eac92625d07e3f9548e33cd7b952a496",
        when="+rocm @1.8.0",
    )

    def setup_build_environment(self, env):
        spec = self.spec
        if spec.satisfies("+sycl"):
            env.set("MKLROOT", join_path(spec["intel-oneapi-mkl"].prefix, "mkl", "latest"))
            env.set("DPL_ROOT", join_path(spec["intel-oneapi-dpl"].prefix, "dpl", "latest"))
            # The `IntelSYCLConfig.cmake` is broken with spack. By default, it
            # relies on the CMAKE_CXX_COMPILER being the real ipcx
            # compiler. If not, the variable SYCL_COMPILER of that script is
            # broken, and all the SYCL detection mechanism is wrong. We fix it
            # by giving hint environment variables.
            env.set("SYCL_LIBRARY_DIR_HINT", os.path.dirname(os.path.dirname(self.compiler.cxx)))
            env.set("SYCL_INCLUDE_DIR_HINT", os.path.dirname(os.path.dirname(self.compiler.cxx)))

    def cmake_args(self):
        # Check that the have the correct C++ standard is available
        if self.spec.satisfies("@:1.2.0"):
            try:
                self.compiler.cxx11_flag
            except UnsupportedCompilerFlag:
                raise InstallError("Ginkgo requires a C++11-compliant C++ compiler")
        else:
            try:
                self.compiler.cxx14_flag
            except UnsupportedCompilerFlag:
                raise InstallError("Ginkgo requires a C++14-compliant C++ compiler")

        if self.spec.satisfies("@1.4.0:1.6.0 +sycl") and not self.spec.satisfies(
            "%oneapi@2021.3.0:"
        ):
            raise InstallError("ginkgo +sycl requires %oneapi@2021.3.0:")
        elif self.spec.satisfies("@1.7.0: +sycl") and not self.spec.satisfies("%oneapi@2022.1.0:"):
            raise InstallError("ginkgo +sycl requires %oneapi@2022.1.0:")
        elif self.spec.satisfies("@1.8.0: +sycl") and not self.spec.satisfies("%oneapi@2023.1.0:"):
            raise InstallError("ginkgo +sycl requires %oneapi@2023.1.0:")

        spec = self.spec
        from_variant = self.define_from_variant
        args = [
            from_variant("GINKGO_BUILD_CUDA", "cuda"),
            from_variant("GINKGO_BUILD_HIP", "rocm"),
            from_variant("GINKGO_BUILD_SYCL", "sycl"),
            from_variant("GINKGO_BUILD_OMP", "openmp"),
            from_variant("GINKGO_BUILD_MPI", "mpi"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("GINKGO_JACOBI_FULL_OPTIMIZATIONS", "full_optimizations"),
            from_variant("GINKGO_BUILD_HWLOC", "hwloc"),
            from_variant("GINKGO_WITH_PAPI_SDE", "sde"),
            from_variant("GINKGO_DEVEL_TOOLS", "develtools"),
            # As we are not exposing benchmarks, examples, tests nor doc
            # as part of the installation, disable building them altogether.
            "-DGINKGO_BUILD_BENCHMARKS=OFF",
            "-DGINKGO_BUILD_DOC=OFF",
            "-DGINKGO_BUILD_EXAMPLES=OFF",
            "-DGINKGO_WITH_CCACHE=OFF",
            self.define("GINKGO_BUILD_TESTS", self.run_tests),
            # Let spack handle the RPATH
            "-DGINKGO_INSTALL_RPATH=OFF",
        ]

        if self.run_tests:
            args.append("-DGINKGO_USE_EXTERNAL_GTEST=ON")

        if spec.satisfies("+cuda"):
            archs = spec.variants["cuda_arch"].value
            if archs != "none":
                arch_str = ";".join(archs)
                args.append("-DGINKGO_CUDA_ARCHITECTURES={0}".format(arch_str))

        if spec.satisfies("+rocm"):
            args.append("-DHIP_PATH={0}".format(spec["hip"].prefix))
            args.append("-DHIP_CLANG_PATH={0}/bin".format(spec["llvm-amdgpu"].prefix))
            args.append("-DHIP_CLANG_INCLUDE_PATH={0}/include".format(spec["llvm-amdgpu"].prefix))
            args.append("-DHIPSPARSE_PATH={0}".format(spec["hipsparse"].prefix))
            args.append("-DHIPBLAS_PATH={0}".format(spec["hipblas"].prefix))
            args.append("-DHIPRAND_PATH={0}/hiprand".format(spec["rocrand"].prefix))
            args.append("-DROCRAND_PATH={0}/rocrand".format(spec["rocrand"].prefix))
            args.append("-DROCPRIM_INCLUDE_DIRS={0}".format(spec["rocprim"].prefix.include))
            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ";".join(archs)
                args.append("-DGINKGO_HIP_AMDGPU={0}".format(arch_str))
            if spec.satisfies("^hip@5.2.0:"):
                args.append(
                    self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)
                )

        if self.spec.satisfies("+sycl"):
            sycl_compatible_compilers = ["icpx"]
            if not (os.path.basename(self.compiler.cxx) in sycl_compatible_compilers):
                raise InstallError("ginkgo +sycl requires icpx compiler.")
        return args

    @property
    def extra_install_tests(self):
        return "test_install" if self.spec.satisfies("@1.3.0") else "test"

    @run_after("install")
    def cache_test_sources(self):
        cache_extra_test_sources(self, self.extra_install_tests)

    def _cached_tests_src_dir(self, script):
        """The cached smoke test source directory for the script."""
        subdir = script if self.spec.satisfies("@1.4.0:") else ""
        return join_path(self.test_suite.current_test_cache_dir, self.extra_install_tests, subdir)

    def _build_and_run_test(self, script):
        """Build and run the test against the installation."""
        src_dir = self._cached_tests_src_dir(script)

        cmake_args = [
            f"-DCMAKE_C_COMPILER={os.environ['CC']}",
            f"-DCMAKE_CXX_COMPILER={os.environ['CXX']}",
            src_dir,
        ]

        # Fix: For HIP tests, add the ARCH compilation flags when not present
        if self.spec.satisfies("+rocm"):
            src_path = join_path(src_dir, "CMakeLists.txt")
            cmakelists = open(src_path, "rt")
            data = cmakelists.read()
            data = data.replace(
                'CLANG_OPTIONS "${GINKGO_PIC_OPTION}"',
                'CLANG_OPTIONS "${GINKGO_AMD_ARCH_FLAGS}" "${GINKGO_PIC_OPTION}"',
            )
            cmakelists.close()
            cmakelists = open(src_path, "wt")
            cmakelists.write(data)
            cmakelists.close()

        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        make = which("make")
        with working_dir(src_dir):
            cmake(*cmake_args)
            make()
            exe = which(script)
            output = exe(output=str.split, error=str.split)
            assert "correctly detected and is complete" in output

    def test_install(self):
        """build, run and check results of test_install"""
        if not self.spec.satisfies("@1.3.0:"):
            raise SkipTest("Test is only available for v1.3.0:")

        self._build_and_run_test("test_install")

    def test_install_cuda(self):
        """build, run and check results of test_install_cuda"""
        if not self.spec.satisfies("@1.4.0: +cuda"):
            raise SkipTest("Test is only available for v1.4.0: +cuda")

        self._build_and_run_test("test_install_cuda")

    def test_install_hip(self):
        """build, run and check results of test_install_hip"""
        if not self.spec.satisfies("@1.4.0: +rocm"):
            raise SkipTest("Test is only available for v1.4.0: +rocm")

        self._build_and_run_test("test_install_hip")

    def test_exportbuild(self):
        """build, run and check results of test_exportbuild"""
        if not self.spec.satisfies("@1.4.0:"):
            raise SkipTest("Test is only available for v1.4.0:")

        self._build_and_run_test("test_exportbuild")
