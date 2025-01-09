# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
from os import path

from llnl.util import filesystem

from spack.package import *


class Hipsycl(CMakePackage, ROCmPackage):
    """hipSYCL is an implementation of the SYCL standard programming model
    over NVIDIA CUDA/AMD HIP"""

    homepage = "https://github.com/illuhad/hipSYCL"
    url = "https://github.com/illuhad/hipSYCL/archive/v0.8.0.tar.gz"
    git = "https://github.com/illuhad/hipSYCL.git"

    provides("sycl")

    license("BSD-2-Clause")

    version("stable", branch="stable", submodules=True)
    version("24.06.0", commit="fc51dae9006d6858fc9c33148cc5f935bb56b075", submodules=True)
    version("24.02.0", commit="974adc33ea5a35dd8b5be68c7a744b37482b8b64", submodules=True)
    version("23.10.0", commit="3952b468c9da89edad9dff953cdcab0a3c3bf78c", submodules=True)
    version("0.9.4", commit="99d9e24d462b35e815e0e59c1b611936c70464ae", submodules=True)
    version("0.9.4", commit="99d9e24d462b35e815e0e59c1b611936c70464ae", submodules=True)
    version("0.9.3", commit="51507bad524c33afe8b124804091b10fa25618dc", submodules=True)
    version("0.9.2", commit="49fd02499841ae884c61c738610e58c27ab51fdb", submodules=True)
    version("0.9.1", commit="fe8465cd5399a932f7221343c07c9942b0fe644c", submodules=True)
    version("0.8.0", commit="2daf8407e49dd32ebd1c266e8e944e390d28b22a", submodules=True)
    version("develop", branch="develop", submodules=True)

    variant("cuda", default=False, description="Enable CUDA backend for SYCL kernels")
    variant("rocm", default=False, description="Enable ROCM backend for SYCL kernels")

    depends_on("cmake@3.5:", type="build")
    depends_on("boost +filesystem", when="@:0.8")
    depends_on("boost@1.67.0:1.69.0 +filesystem +fiber +context cxxstd=17", when="@0.9.1:")
    depends_on("python@3:")
    depends_on("llvm@8: +clang", when="~cuda")
    depends_on("llvm@9: +clang", when="+cuda")
    # hipSYCL 0.8.0 supported only LLVM 8-10:
    # (https://github.com/AdaptiveCpp/AdaptiveCpp/blob/v0.8.0/CMakeLists.txt#L29-L37)
    depends_on("llvm@8:10", when="@0.8.0")
    # https://github.com/spack/spack/issues/45029 and https://github.com/spack/spack/issues/43142
    conflicts("^gcc@12", when="@23.10.0")
    # https://github.com/OpenSYCL/OpenSYCL/pull/918 was introduced after 0.9.4
    conflicts("^gcc@12.2.0", when="@:0.9.4")
    # LLVM PTX backend requires cuda7:10.1 (https://tinyurl.com/v82k5qq)
    depends_on("cuda@9:10.1", when="@0.8.1: +cuda ^llvm@9")
    depends_on("cuda@9:", when="@0.8.1: +cuda ^llvm@10:")
    # hipSYCL@:0.8.0 requires cuda@9:10.0 due to a known bug
    depends_on("cuda@9:10.0", when="@:0.8.0 +cuda")

    conflicts(
        "%gcc@:4",
        when="@:0.9.0",
        msg="hipSYCL needs proper C++14 support to be built, %gcc is too old",
    )
    conflicts(
        "%gcc@:8",
        when="@0.9.1:",
        msg="hipSYCL needs proper C++17 support to be built, %gcc is too old",
    )
    conflicts(
        "^llvm build_type=Debug",
        when="+cuda",
        msg="LLVM debug builds don't work with hipSYCL CUDA backend; for "
        "further info please refer to: "
        "https://github.com/illuhad/hipSYCL/blob/master/doc/install-cuda.md",
    )
    # https://github.com/spack/spack/issues/46681
    conflicts("^llvm@19", when="@24.02.0:24.06.0")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_CPU_BACKEND:Bool=TRUE",
            "-DWITH_ROCM_BACKEND:Bool={0}".format("TRUE" if spec.satisfies("+rocm") else "FALSE"),
            "-DWITH_CUDA_BACKEND:Bool={0}".format("TRUE" if spec.satisfies("+cuda") else "FALSE"),
            # prevent hipSYCL's cmake to look for other LLVM installations
            # if the specified one isn't compatible
            "-DDISABLE_LLVM_VERSION_CHECK:Bool=TRUE",
        ]
        # LLVM directory containing all installed CMake files
        # (e.g.: configs consumed by client projects)
        llvm_cmake_dirs = filesystem.find(spec["llvm"].prefix, "LLVMExports.cmake")
        if len(llvm_cmake_dirs) != 1:
            raise InstallError(
                "concretized llvm dependency must provide "
                "a unique directory containing CMake client "
                "files, found: {0}".format(llvm_cmake_dirs)
            )
        args.append("-DLLVM_DIR:String={0}".format(path.dirname(llvm_cmake_dirs[0])))
        # clang internal headers directory
        llvm_clang_include_dirs = filesystem.find(
            spec["llvm"].prefix, "__clang_cuda_runtime_wrapper.h"
        )
        if len(llvm_clang_include_dirs) != 1:
            raise InstallError(
                "concretized llvm dependency must provide a "
                "unique directory containing clang internal "
                "headers, found: {0}".format(llvm_clang_include_dirs)
            )
        args.append(
            "-DCLANG_INCLUDE_PATH:String={0}".format(path.dirname(llvm_clang_include_dirs[0]))
        )
        # target clang++ executable
        llvm_clang_bin = path.join(spec["llvm"].prefix.bin, "clang++")
        if not filesystem.is_exe(llvm_clang_bin):
            raise InstallError(
                "concretized llvm dependency must provide a "
                "valid clang++ executable, found invalid: "
                "{0}".format(llvm_clang_bin)
            )
        args.append("-DCLANG_EXECUTABLE_PATH:String={0}".format(llvm_clang_bin))
        # explicit CUDA toolkit
        if spec.satisfies("+cuda"):
            args.append("-DCUDA_TOOLKIT_ROOT_DIR:String={0}".format(spec["cuda"].prefix))
        if spec.satisfies("+rocm"):
            args.append("-DWITH_ACCELERATED_CPU:STRING=OFF")
            args.append("-DROCM_PATH:STRING={0}".format(os.environ.get("ROCM_PATH")))
            if self.spec.satisfies("@24.02.0:"):
                args.append("-DWITH_SSCP_COMPILER=OFF")
        return args

    @run_after("install")
    def filter_config_file(self):
        def edit_config(filename, editor):
            config_file_paths = filesystem.find(self.prefix, filename)
            if len(config_file_paths) != 1:
                raise InstallError(
                    "installed hipSYCL must provide a unique compiler driver"
                    "configuration file ({0}), found: {1}".format(filename, config_file_paths)
                )
            config_file_path = config_file_paths[0]
            with open(config_file_path) as f:
                config = json.load(f)

            config_modified = editor(config)

            with open(config_file_path, "w") as f:
                json.dump(config_modified, f, indent=2)

        if self.spec.satisfies("@:23.10.0"):
            configfiles = {"core": "syclcc.json", "cuda": "syclcc.json"}
        else:
            configfiles = {"core": "acpp-core.json", "cuda": "acpp-cuda.json"}

        def adjust_core_config(config):
            config["default-cpu-cxx"] = self.compiler.cxx
            return config

        edit_config(configfiles["core"], adjust_core_config)

        if self.spec.satisfies("+cuda"):
            # 1. Fix compiler: use the real one in place of the Spack wrapper

            # 2. Fix stdlib: we need to make sure cuda-enabled binaries find
            #    the libc++.so and libc++abi.so dyn linked to the sycl
            #    ptx backend
            rpaths = set()
            if self.spec.satisfies("~rocm"):
                so_paths = filesystem.find_libraries(
                    "libc++", self.spec["llvm"].prefix, shared=True, recursive=True
                )
                if len(so_paths) != 1:
                    raise InstallError(
                        "concretized llvm dependency must provide a "
                        "unique directory containing libc++.so, "
                        "found: {0}".format(so_paths)
                    )
                rpaths.add(path.dirname(so_paths[0]))
                so_paths = filesystem.find_libraries(
                    "libc++abi", self.spec["llvm"].prefix, shared=True, recursive=True
                )
                if len(so_paths) != 1:
                    raise InstallError(
                        "concretized llvm dependency must provide a "
                        "unique directory containing libc++abi, "
                        "found: {0}".format(so_paths)
                    )
                rpaths.add(path.dirname(so_paths[0]))

                def adjust_cuda_config(config):
                    config["default-cuda-link-line"] += " " + " ".join(
                        "-rpath {0}".format(p) for p in rpaths
                    )
                    return config

                edit_config(configfiles["cuda"], adjust_cuda_config)
