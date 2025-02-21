# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
from os import path

from llnl.util import filesystem

from spack.package import *


class Adaptivecpp(CMakePackage, ROCmPackage):
    """AdaptiveCpp is an implementation of SYCL and C++ standard parallelism for CPUs and GPUs
    from all vendors: The independent, community-driven compiler for C++-based heterogeneous
    programming models.
    Lets applications adapt themselves to all the hardware in the system - even at runtime!

    This package has been previously known as hipSYCL and, briefly, Open SYCL.
    """

    homepage = "https://adaptivecpp.github.io/"
    url = "https://github.com/AdaptiveCpp/AdaptiveCpp/archive/refs/tags/v24.10.0.tar.gz"
    git = "https://github.com/AdaptiveCpp/AdaptiveCpp.git"

    provides("sycl")

    license("BSD-2-Clause")

    with default_args(submodules=True):
        version("stable", branch="stable")
        version("develop", branch="develop")
        version("24.10.0", commit="7677cf6eefd8ab46d66168cd07ab042109448124")
        # AdaptiveCpp only officially supports the latest version
        # but we don't deprecate everything else just yet
        version("24.06.0", commit="fc51dae9006d6858fc9c33148cc5f935bb56b075")
        version("24.02.0", commit="974adc33ea5a35dd8b5be68c7a744b37482b8b64")
        version("23.10.0", commit="3952b468c9da89edad9dff953cdcab0a3c3bf78c")

    variant("cuda", default=False, description="Enable CUDA backend for SYCL kernels")
    variant("rocm", default=False, description="Enable ROCM backend for SYCL kernels")

    depends_on("cmake@3.5:", type="build")
    depends_on("cmake@3.9:", type="build", when="@24.06:")
    depends_on("cmake@3.10:", type="build", when="@24.10:")

    depends_on("boost@1.67: +filesystem +fiber +context cxxstd=17", when="@23.10:")
    depends_on("python@3:")
    depends_on("llvm@8: +clang", when="~cuda")
    depends_on("llvm@9: +clang", when="+cuda")
    # https://github.com/spack/spack/issues/45029 and https://github.com/spack/spack/issues/43142
    conflicts("^gcc@12", when="@23.10.0")
    # LLVM PTX backend requires cuda7:10.1 (https://tinyurl.com/v82k5qq)
    depends_on("cuda@9:10.1", when="@23.10.0: +cuda ^llvm@9")
    depends_on("cuda@9:", when="@23.10.0: +cuda ^llvm@10:")

    conflicts("%gcc@:8", msg="AdaptiveCpp needs proper C++17 support to be built, %gcc is too old")
    conflicts(
        "^llvm build_type=Debug",
        when="+cuda",
        msg="LLVM debug builds don't work with AdaptiveCpp CUDA backend; for "
        "further info please refer to: "
        "https://github.com/AdaptiveCpp/AdaptiveCpp/blob/master/doc/install-cuda.md",
    )
    # https://github.com/spack/spack/issues/46681
    conflicts("^llvm@19", when="@24.02.0:24.06.0")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_CPU_BACKEND:Bool=TRUE",
            "-DWITH_ROCM_BACKEND:Bool={0}".format("TRUE" if spec.satisfies("+rocm") else "FALSE"),
            "-DWITH_CUDA_BACKEND:Bool={0}".format("TRUE" if spec.satisfies("+cuda") else "FALSE"),
            # prevent AdaptiveCpp's cmake to look for other LLVM installations
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
                    "installed AdaptiveCpp must provide a unique compiler driver"
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
