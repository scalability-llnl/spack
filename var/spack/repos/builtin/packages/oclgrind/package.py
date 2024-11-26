# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Oclgrind(CMakePackage):
    """An OpenCL device simulator and debugger."""

    homepage = "https://github.com/jrprice/Oclgrind"
    url = "https://github.com/jrprice/Oclgrind/archive/v19.10.tar.gz"
    git = "https://github.com/jrprice/Oclgrind"

    maintainers("matthiasdiener")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("19.10", sha256="f9a8f22cb9f6d88670f2578c46ba0d728ba8eaee5c481c2811129dc157c43dc0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("llvm +clang @5.0:")
