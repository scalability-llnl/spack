# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Haccabana(CMakePackage):
    """HACCabana: A proxy app for HACC short range forces.
    The Hardware/Hybrid Accelerated Cosmology Code (HACC), a cosmology
    N-body-code framework, is designed to run efficiently on diverse computing
    architectures and to scale to millions of cores and beyond."""

    homepage = "https://github.com/ECP-CoPA/HACCabana"
    git = "https://github.com/ECP-CoPA/HACCabana.git"

    maintainers("steverangel", "adrianpope", "streeve", "junghans")

    tags = ["proxy-app", "ecp-proxy-app"]

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")

    depends_on("cmake@3.9:", type="build")
    depends_on("kokkos@3.0:")
    depends_on("cabana@master")

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        return options
