# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

import spack.build_systems.cmake
from spack.package import *


class HipTests(CMakePackage):
    """This repository provides unit tests for HIP implementation."""

    homepage = "https://github.com/ROCm/hip-tests"
    url = "https://github.com/ROCm/hip-tests/archive/refs/tags/rocm-6.1.2.tar.gz"
    git = "https://github.com/ROCm/hip-tests.git"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    version("6.3.1", sha256="0fc1cf4f46f2bbef377d65803d86c2489b01b598c468070c79c5114a661f07c6")
    version("6.3.0", sha256="8081d4ab1a43ffa1cebd646668d83008b799ab98c14daf7b455922355a439c8a")
    version("6.2.4", sha256="1478b49583d09cb3a96e26ec3bf8dc5ff3e3ec72fa133bb6d7768595d825051e")
    version("6.2.1", sha256="90fcf0169889533b882d289f9cb8a7baf9bd46a3ce36752b915083931dc839f1")
    version("6.2.0", sha256="314837dbac78be71844ceb959476470c484fdcd4fb622ff8de9277783e0fcf1c")
    version("6.1.2", sha256="5b14e4a30d8d8fb56c43e262009646ba9188eac1c8ff882d9a606a4bec69b56b")
    version("6.1.1", sha256="10c96ee72adf4580056292ab17cfd858a2fd7bc07abeb41c6780bd147b47f7af")
    version("6.1.0", sha256="cf3a6a7c43116032d933cc3bc88bfc4b17a4ee1513c978e751755ca11a5ed381")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("cmake", type="run")

    for ver in ["6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1", "6.2.4", "6.3.0", "6.3.1"]:
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", when=f"@{ver}")
        depends_on(f"hipify-clang@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

    root_cmakelists_dir = "catch"

    def patch(self):
        filter_file(
            "${ROCM_PATH}/bin/rocm_agent_enumerator",
            f"{self.spec['rocminfo'].prefix}/bin/rocm_agent_enumerator",
            "catch/CMakeLists.txt",
            string=True,
        )
        filter_file(
            "/opt/rocm/bin/rocm_agent_enumerator",
            f"{self.spec['rocminfo'].prefix}/bin/rocm_agent_enumerator",
            "catch/hipTestMain/hip_test_context.cc",
            string=True,
        )
        filter_file(
            "${HIP_PATH}/llvm",
            self.spec["llvm-amdgpu"].prefix,
            "samples/2_Cookbook/17_llvm_ir_to_executable/CMakeLists.txt",
            "samples/2_Cookbook/16_assembly_to_executable/CMakeLists.txt",
            string=True,
        )
        filter_file(
            "${ROCM_PATH}/llvm",
            self.spec["llvm-amdgpu"].prefix,
            "catch/CMakeLists.txt",
            "samples/2_Cookbook/16_assembly_to_executable/CMakeLists.txt",
            "samples/2_Cookbook/21_cmake_hip_cxx_clang/CMakeLists.txt",
            "samples/2_Cookbook/18_cmake_hip_device/CMakeLists.txt",
            "samples/2_Cookbook/17_llvm_ir_to_executable/CMakeLists.txt",
            "samples/2_Cookbook/23_cmake_hiprtc/CMakeLists.txt",
            "samples/2_Cookbook/22_cmake_hip_lang/CMakeLists.txt",
            "samples/2_Cookbook/19_cmake_lang/CMakeLists.txt",
            string=True,
        )
        filter_file(
            "${CMAKE_PREFIX_PATH}/bin/hipify-perl",
            f"{self.spec['hipify-clang'].prefix.bin}/hipify-perl",
            "samples/0_Intro/square/CMakeLists.txt",
            string=True,
        )

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("HIP_PLATFORM", "amd"),
            self.define("HIP_PATH", self.spec["hip"].prefix),
            self.define("ROCM_PATH", self.spec["hip"].prefix),
        ]
        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("build_tests")

    @run_after("install")
    def cache_test_sources(self):
        """Copy the tests source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, "samples")

    def test_samples(self):
        """build and run all hip samples"""
        sample_test_binaries = [
            "0_Intro/bit_extract/bit_extract",
            "0_Intro/module_api/launchKernelHcc.hip.out",
            "0_Intro/module_api/runKernel.hip.out",
            "0_Intro/module_api/defaultDriver.hip.out",
            "0_Intro/module_api_global/runKernel1.hip.out",
            "0_Intro/square/square",
            "1_Utils/hipDispatchLatency/hipDispatchEnqueueRateMT",
            "1_Utils/hipDispatchLatency/hipDispatchLatency",
            "1_Utils/hipInfo/hipInfo",
            "2_Cookbook/0_MatrixTranspose/MatrixTranspose",
            "2_Cookbook/1_hipEvent/hipEvent",
            "2_Cookbook/3_shared_memory/sharedMemory",
            "2_Cookbook/4_shfl/shfl",
            "2_Cookbook/5_2dshfl/2dshfl",
            "2_Cookbook/6_dynamic_shared/dynamic_shared",
            "2_Cookbook/8_peer2peer/peer2peer",
            "2_Cookbook/9_unroll/unroll",
            "2_Cookbook/10_inline_asm/inline_asm",
            "2_Cookbook/11_texture_driver/texture2dDrv",
            "2_Cookbook/12_cmake_hip_add_executable/MatrixTranspose1",
            "2_Cookbook/13_occupancy/occupancy",
            "2_Cookbook/14_gpu_arch/gpuarch",
            "2_Cookbook/15_static_library/device_functions/test_device_static",
            "2_Cookbook/15_static_library/host_functions/test_opt_static",
            "2_Cookbook/16_assembly_to_executable/square_asm.out",
            "2_Cookbook/17_llvm_ir_to_executable/square_ir.out",
            "2_Cookbook/18_cmake_hip_device/test_cpp",
            "2_Cookbook/19_cmake_lang/test_cpp1",
            "2_Cookbook/19_cmake_lang/test_fortran",
            "2_Cookbook/21_cmake_hip_cxx_clang/square1",
            "2_Cookbook/22_cmake_hip_lang/square2",
            "2_Cookbook/23_cmake_hiprtc/test",
        ]

        test_dir = join_path(self.test_suite.current_test_cache_dir, "samples")
        prefix_paths = ";".join(spack.build_systems.cmake.get_cmake_prefix_path(self))
        clang_cpp_path = join_path(self.spec["llvm-amdgpu"].prefix, "bin", "clang++")
        clang_path = join_path(self.spec["llvm-amdgpu"].prefix, "bin", "clang")
        cc_options = [
            f"-DCMAKE_MODULE_PATH={self.spec['hip'].prefix.lib.cmake.hip}",
            f"-DCMAKE_PREFIX_PATH={prefix_paths}",
            f"-DCMAKE_CXX_COMPILER={clang_cpp_path}",
            f"-DCMAKE_C_COMPILER={clang_path}",
            f"-DHIP_HIPCC_EXECUTABLE={self.spec['hip'].prefix.bin}/hipcc",
            f"-DCMAKE_HIP_COMPILER_ROCM={clang_cpp_path}",
            ".",
        ]

        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        with working_dir(test_dir, create=True):
            cmake(*cc_options)
            make("build_samples")
            for binary_path in sample_test_binaries:
                # binaries need to run in their directories
                bin_dir, binary = os.path.split(binary_path)
                with working_dir(bin_dir, create=True):
                    with test_part(
                        self,
                        "test_sample_{0}".format(binary),
                        purpose="configure, build and run test: {0}".format(binary),
                    ):
                        exe = Executable(binary)
                        if binary == "hipDispatchEnqueueRateMT":
                            options = ["16", "0"]
                        else:
                            options = []
                        exe(*options)
