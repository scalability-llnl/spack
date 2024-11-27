# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Fpchecker(CMakePackage):
    """FPChecker (Floating-Point Checker) is a dynamic analysis tool
    to detect floating-point errors in HPC applications.
    """

    homepage = "https://fpchecker.org/"
    url = "https://github.com/LLNL/FPChecker/archive/refs/tags/v0.3.4.tar.gz"
    git = "https://github.com/LLNL/FPChecker.git"

    maintainers("ilagunap")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.4.0", sha256="59d18a3fb5211645bb1cfde1502ba78a9cca4234604dfd879534d7f13ae5d5b9")
    version("0.3.5", sha256="ed7277318af8e0a22b05c5655c9acc99e1d3036af41095ec2f1b1ada4d6e90f6")
    version("0.3.4", sha256="ecea778dcddc8347da86b02069e12d574a3ba27a4f7c6224bf492fbff6cd162a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("llvm@12.0.1")
    depends_on("cmake@3.4:", type="build")
    depends_on("python@3:", type="run")

    def cmake_args(self):
        args = ["-DCMAKE_C_COMPILER=clang", "-DCMAKE_CXX_COMPILER=clang++"]
        return args
