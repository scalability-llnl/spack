# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IntelLlvm(CMakePackage):
    """Intel's version of the LLVM compiler."""

    maintainers("rscohn2")

    homepage = "https://github.com/intel/llvm"
    git = "https://github.com/intel/llvm.git"

    license("Apache-2.0")

    version("sycl", branch="sycl")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.4.3:", type="build")

    # It doesn't seem possible to use != in a conflicts statement
    # conflicts('target != x86_64',
    #            msg='Intel LLVM compiler currently only works for x86')

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", self.compiler.cxx11_flag)

    def setup_run_environment(self, env):
        if self.spec.satisfies("+clang"):
            env.set("CC", join_path(self.spec.prefix.bin, "clang"))
            env.set("CXX", join_path(self.spec.prefix.bin, "clang++"))

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        cmake_args = []

        cmake_args.extend(
            [
                "-DLLVM_TARGETS_TO_BUILD=X86",
                "-DLLVM_EXTERNAL_PROJECTS=llvm-spirv;sycl",
                "-DLLVM_ENABLE_PROJECTS=clang;llvm-spirv;sycl",
                "-DLLVM_EXTERNAL_SYCL_SOURCE_DIR={0}".format(
                    join_path(self.stage.source_path, "sycl")
                ),
                "-DLLVM_EXTERNAL_LLVM_SPIRV_SOURCE_DIR={0}".format(
                    join_path(self.stage.source_path, "llvm-spirv")
                ),
            ]
        )

        return cmake_args
