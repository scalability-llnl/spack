# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import UnsupportedCompilerFlag
from spack.package import *


class Taskflow(CMakePackage):
    """Taskflow helps you quickly write parallel tasks programs in
    modern C++."""

    homepage = "https://github.com/taskflow/taskflow"
    url = "https://github.com/taskflow/taskflow/archive/v2.7.0.tar.gz"
    git = "https://github.com/taskflow/taskflow.git"

    license("MIT")

    version("master", branch="master")
    version("3.7.0", sha256="788b88093fb3788329ebbf7c7ee05d1f8960d974985a301798df01e77e04233b")
    version("3.6.0", sha256="5a1cd9cf89f93a97fcace58fd73ed2fc8ee2053bcb43e047acb6bc121c3edf4c")
    version("2.7.0", sha256="bc2227dcabec86abeba1fee56bb357d9d3c0ef0184f7c2275d7008e8758dfc3e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Compiler must offer C++14 support
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")
    conflicts("%apple-clang@:8.0.0")
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag:
            InstallError("Taskflow requires a C++14-compliant C++ compiler")

        args = []
        return args
