# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chaco(CMakePackage):
    """Graph partitioning library"""

    homepage = "https://gitlab.com/truchas/tpl-forks/chaco"
    git = "https://gitlab.com/truchas/tpl-forks/chaco.git"

    maintainers("pbrady", "zjibben")

    license("LGPL-2.1-or-later")

    version("develop", branch="truchas")
    version("2020-07-16", commit="92a877b381933d12b02507413897f696d81b4682", preferred=True)

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="build shared library")

    depends_on("cmake@3.16:", type="build")

    def cmake_args(self):
        opts = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        if self.spec.satisfies("%apple-clang@12:"):
            opts.append(self.define("CMAKE_C_FLAGS", "-Wno-error=implicit-function-declaration"))
        return opts
