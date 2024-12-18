# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tethex(CMakePackage):
    """Tethex is designed to convert triangular (in 2D) or tetrahedral (in 3D)
    Gmsh's mesh to quadrilateral or hexahedral one respectively. These meshes
    can be used in software packages working with hexahedrals only - for
    example, deal.II.
    """

    homepage = "https://github.com/martemyev/tethex"
    url = "https://github.com/martemyev/tethex/archive/v0.0.7.tar.gz"
    git = "https://github.com/martemyev/tethex.git"

    version("develop", branch="master")
    version("0.0.7", sha256="5f93f434c6d110be3d8d0eba69336864d0e5a26aba2d444eb25adbd2caf73645")

    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    depends_on("cmake@2.8:", type="build")

    def install(self, spec, prefix):
        # install by hand
        mkdirp(prefix.bin)
        install("tethex", prefix.bin)
