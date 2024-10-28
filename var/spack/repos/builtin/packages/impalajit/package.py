# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Impalajit(CMakePackage):
    """A lightweight JIT compiler for flexible data access in simulation applications.
    impalajit@llvm is enhanced with LLVM JIT. This means that impalajit@llvm is
    supposed to work on any architecture supported by llvm, contrary to the
    impalajit@main package which is restricted to x86 architectures.This comes at the
    price of extra dependencies. Impala acts as a backend for `easi` project."""

    homepage = "https://github.com/manuel-fasching/ImpalaJIT/blob/master/README.md"

    license("MIT-0")

    version(
        "main",
        git="https://github.com/manuel-fasching/ImpalaJIT.git",
        branch="master",
        preferred=True,
    )
    version("llvm", git="https://github.com/ravil-mobile/ImpalaJIT.git", branch="dev")
    version("llvm-1.0.0", git="https://github.com/ravil-mobile/ImpalaJIT.git", tag="v1.0.0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    maintainers("ravil-mobile", "Thomas-Ulrich")

    variant("shared", default=True, description="build as a shared library")
    depends_on("cmake", type="build")
    depends_on("pkgconfig", type="build", when="@main")
    depends_on("llvm@10.0.0:11.1.0", when="@llvm")
    depends_on("z3", when="@llvm")
    depends_on("llvm@10.0.0:11.1.0", when="@llvm-1.0.0")
    depends_on("z3", when="@llvm-1.0.0")

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("SHARED_LIB", "shared"))
        args.append(self.define("TESTS", self.run_tests))

        if not self.spec.satisfies("%intel"):
            args.append("-DINTEL_COMPILER=OFF")
        return args
