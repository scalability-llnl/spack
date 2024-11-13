# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Perfstubs(CMakePackage):
    """Profiling API for adding tool instrumentation support to any project.

    This was motivated by the need to quickly add instrumentation to the
    [ADIOS2](https://github.com/ornladios/ADIOS2) library without adding a build
    dependency, or tying to a specific measurement tool.

    The initial prototype implementation was tied to TAU, but evolved to this more
    generic version, which was extracted as a separate repository for testing and
    demonstration purposes.
    """

    homepage = "https://github.com/khuck/perfstubs"
    git = "https://github.com/khuck/perfstubs.git"

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    variant("static", default=False, description="Build static executable support")

    def cmake_args(self):
        args = [self.define_from_variant("PERFSTUBS_USE_STATIC", "static")]
        return args
