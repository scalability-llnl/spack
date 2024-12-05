# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Binder(CMakePackage):
    """
    Binder is a tool for automatic generation of Python bindings
    for C++11 projects using Pybind11 and Clang LibTooling libraries.
    That is, Binder, takes a C++ project and compiles it into objects
    and functions that are all usable within Python.
    Binder is different from prior tools in that it handles special
    features new in C++11.
    """

    homepage = "https://github.com/RosettaCommons/binder"
    git = "https://github.com/RosettaCommons/binder.git"

    maintainers("lyskov", "kliegeois")

    license("MIT")

    version("master", branch="master")
    version("1.4.2", tag="v1.4.2", commit="b9f309e0513e745a7465571321e87595fa33d195")
    version("1.3.0", tag="v1.3.0", commit="e9b55985af297ca161d615058e4a5da07c22bc77")
    version("1.2.0", tag="v1.2.0", commit="90cf5b31b6f4ecad3fe87518ca2b949dc9e8ed1a")
    version("1.1.0", tag="v1.0.0", commit="3de7949343197295250f988716d511a264b21324")
    version("1.0.0", tag="v1.0.0", commit="3de7949343197295250f988716d511a264b21324")

    depends_on("cxx", type="build")  # generated

    # Add dependencies
    depends_on("llvm+clang+llvm_dylib@7.0:9", when="@:1.3.0")
    depends_on("llvm+clang+llvm_dylib@7.0:", when="@1.4.2:")

    patch("llvm_dir.patch", when="@1.4.2:")

    def cmake_args(self):
        spec = self.spec
        llvm_dir = spec["llvm"].prefix
        clang_dir = spec["llvm"].prefix
        options = []

        options.extend(
            [
                "-DLLVM_DIR:FILEPATH={0}".format(llvm_dir),
                "-DClang_DIR:FILEPATH={0}".format(clang_dir),
                "-DCMAKE_CXX_FLAGS=-Wl,--verbose",
                "-DBINDER_ENABLE_TEST=OFF",
            ]
        )
        return options

    def setup_dependent_package(self, module, dependent_spec):
        llvm_dir = self.spec["llvm"].prefix
        self.spec.clang_include_dirs = llvm_dir.include
        self.spec.libclang_include_dir = llvm_dir.lib.clang.join(
            format(self.spec["llvm"].version)
        ).include
