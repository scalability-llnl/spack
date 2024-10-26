# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Voropp(CMakePackage):
    """Voro++ is a open source software library for the computation of the
    Voronoi diagram, a widely-used tessellation that has applications in many
    scientific fields."""

    homepage = "https://math.lbl.gov/voro++/about.html"
    url = "https://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz"
    git = "https://github.com/chr1shr/voro"

    variant("shared", default=True, description="Build shared libraries")

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")
    version("0.4.6", sha256="ef7970071ee2ce3800daa8723649ca069dc4c71cc25f0f7d22552387f3ea437e")

    depends_on("cxx", type="build")  # generated

    patch("voro++-0.4.6-cmake.patch", when="@0.4.6")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        return args
