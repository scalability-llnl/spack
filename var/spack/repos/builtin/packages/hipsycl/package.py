# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os import path
import json
from llnl.util import filesystem


class Hipsycl(CMakePackage):
    """hipSYCL is an implementation of the SYCL standard programming model
    over NVIDIA CUDA/AMD HIP"""

    homepage = "https://github.com/illuhad/hipSYCL"
    url = "https://github.com/illuhad/hipSYCL/archive/v0.8.0.tar.gz"
    git = "https://github.com/illuhad/hipSYCL.git"

    maintainers = ["nazavode"]

    provides("sycl")

    version("stable", branch="stable", submodules=True)
    version(
        "0.9.1",
        commit="fe8465cd5399a932f7221343c07c9942b0fe644c",
        submodules=True)
    version(
        "0.8.0",
        commit="2daf8407e49dd32ebd1c266e8e944e390d28b22a",
        submodules=True,
    )

    variant(
        "cuda",
        default=False,
        description="Enable CUDA backend for SYCL kernels",
    )

    depends_on("cmake@3.5:", type="build")
    depends_on("boost +filesystem", when="@:0.8.99")
    depends_on("boost@1.67.0:1.69.0 +filesystem +fiber +context cxxstd=17", when='@0.9.1:')
    depends_on("python@3:")
    depends_on("llvm@8: +clang", when="~cuda")
    depends_on("llvm@9: +clang", when="+cuda")
    # LLVM PTX backend requires cuda7:10.1.9999 (https://tinyurl.com/v82k5qq)
    depends_on("cuda@9:10.1.9999", when="@0.8.1: +cuda")
    # hipSYCL@:0.8.0 requires cuda@9:10.0.9999 due to a known bug
    depends_on("cuda@9:10.0.9999", when="@:0.8.0 +cuda")

    conflicts(
        "%gcc@:4.9999",
        when='@:0.9.0',
        msg="hipSYCL needs proper C++14 support to be built, %gcc is too old",
    )
    conflicts(
        "%gcc@:8.9999",
        when='@0.9.1:',
        msg="hipSYCL needs proper C++17 support to be built, %gcc is too old")
    conflicts(
        "^llvm build_type=Debug",
        when="+cuda",
        msg="LLVM debug builds don't work with hipSYCL CUDA backend; for "
        "further info please refer to: "
        "https://github.com/illuhad/hipSYCL/blob/master/doc/install-cuda.md",
    )

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_CPU_BACKEND:Bool=TRUE",
            # TODO: no ROCm stuff available in spack yet
            "-DWITH_ROCM_BACKEND:Bool=FALSE",
            "-DWITH_CUDA_BACKEND:Bool={0}".format(
                "TRUE" if "+cuda" in spec else "FALSE"
            ),
            # prevent hipSYCL's cmake to look for other LLVM installations
            # if the specified one isn't compatible
            "-DDISABLE_LLVM_VERSION_CHECK:Bool=TRUE",
        ]
        # LLVM directory containing all installed CMake files
        # (e.g.: configs consumed by client projects)
        llvm_cmake_dirs = filesystem.find(
            spec["llvm"].prefix, "LLVMExports.cmake"
        )
        if len(llvm_cmake_dirs) != 1:
            raise InstallError(
                "concretized llvm dependency must provide "
                "a unique directory containing CMake client "
                "files, found: {0}".format(llvm_cmake_dirs)
            )
        args.append(
            "-DLLVM_DIR:String={0}".format(path.dirname(llvm_cmake_dirs[0]))
        )
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
            "-DCLANG_INCLUDE_PATH:String={0}".format(
                path.dirname(llvm_clang_include_dirs[0])
            )
        )
        # target clang++ executable
        llvm_clang_bin = path.join(spec["llvm"].prefix.bin, "clang++")
        if not filesystem.is_exe(llvm_clang_bin):
            raise InstallError(
                "concretized llvm dependency must provide a "
                "valid clang++ executable, found invalid: "
                "{0}".format(llvm_clang_bin)
            )
        args.append(
            "-DCLANG_EXECUTABLE_PATH:String={0}".format(llvm_clang_bin)
        )
        # explicit CUDA toolkit
        if "+cuda" in spec:
            args.append(
                "-DCUDA_TOOLKIT_ROOT_DIR:String={0}".format(
                    spec["cuda"].prefix
                )
            )
        return args

    @run_after("install")
    def filter_config_file(self):
        config_file_paths = filesystem.find(self.prefix, "syclcc.json")
        if len(config_file_paths) != 1:
            raise InstallError(
                "installed hipSYCL must provide a unique compiler driver "
                "configuration file, found: {0}".format(config_file_paths)
            )
        config_file_path = config_file_paths[0]
        with open(config_file_path) as f:
            config = json.load(f)
        # 1. Fix compiler: use the real one in place of the Spack wrapper
        config["default-cpu-cxx"] = self.compiler.cxx
        # 2. Fix stdlib: we need to make sure cuda-enabled binaries find
        #    the libc++.so and libc++abi.so dyn linked to the sycl
        #    ptx backend
        rpaths = set()
        so_paths = filesystem.find(self.spec["llvm"].prefix, "libc++.so")
        if len(so_paths) != 1:
            raise InstallError(
                "concretized llvm dependency must provide a "
                "unique directory containing libc++.so, "
                "found: {0}".format(so_paths)
            )
        rpaths.add(path.dirname(so_paths[0]))
        so_paths = filesystem.find(self.spec["llvm"].prefix, "libc++abi.so")
        if len(so_paths) != 1:
            raise InstallError(
                "concretized llvm dependency must provide a "
                "unique directory containing libc++abi.so, "
                "found: {0}".format(so_paths)
            )
        rpaths.add(path.dirname(so_paths[0]))
        config["default-cuda-link-line"] += " " + " ".join(
            "-rpath {0}".format(p) for p in rpaths
        )
        # Replace the installed config file
        with open(config_file_path, "w") as f:
            json.dump(config, f, indent=2)
