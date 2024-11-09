# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Archer(CMakePackage):
    """ARCHER, a data race detection tool for large OpenMP applications."""

    homepage = "https://github.com/PRUNERS/ARCHER"
    url = "https://github.com/PRUNERS/archer/archive/v1.0.0.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True

    version("2.0.0", sha256="3241cadb0078403368b69166b27f815e12c350486d4ceb3fb33147895b9ebde8")
    version("1.0.0", sha256="df814a475606b83c659932caa30a68bed1c62e713386b375c1b78eb8d60e0d15")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.4.3:", type="build")
    depends_on("llvm@:8.0.0")
    depends_on("ninja@1.5:", type="build")
    depends_on("llvm-openmp-ompt@tr6_forwards")

    generator("ninja")

    def patch(self):
        if self.spec.satisfies("^llvm@8.0.0:"):
            filter_file(
                r"add_llvm_loadable_module\(LLVMArcher",
                "add_llvm_library(LLVMArcher MODULE",
                "lib/CMakeLists.txt",
            )

    def cmake_args(self):
        return [
            self.define("CMAKE_C_COMPILER", "clang"),
            self.define("CMAKE_CXX_COMPILER", "clang++"),
            self.define("OMP_PREFIX:PATH", self.spec["llvm-openmp-ompt"].prefix),
        ]

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, ["test"])

    def test_run_parallel_example(self):
        """build and run parallel-simple"""
        test_dir = join_path(self.test_suite.current_test_cache_dir, "test", "parallel")
        if not os.path.exists(test_dir):
            raise SkipTest("Parallel test directory does not exist")

        test_exe = "parallel-simple"
        test_src = f"{test_exe}.c"
        with working_dir(test_dir):
            clang = which("clang-archer")
            clang("-o", test_exe, test_src)

            parallel_simple = which(test_exe)
            parallel_simple()
