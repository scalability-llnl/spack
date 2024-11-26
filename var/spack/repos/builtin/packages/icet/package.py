# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Icet(CMakePackage):
    """The Image Composition Engine for Tiles (IceT) is a high-performance
    sort-last parallel rendering library."""

    homepage = "https://icet.sandia.gov"
    url = "https://gitlab.kitware.com/api/v4/projects/icet%2Ficet/repository/archive.tar.bz2?sha=IceT-2.1.1"
    git = "https://gitlab.kitware.com/icet/icet.git"

    version("develop", branch="master")
    version("2.1.1", sha256="04cc5b7aa5b3ec95b255febdcfc2312e553ce3db5ca305526803d5737561ec32")

    depends_on("c", type="build")  # generated

    variant("opengl", default=False, description="Use opengl")
    variant("shared", default=True, description="Enable shared library")

    depends_on("mpi")
    depends_on("gl", when="+opengl")

    def cmake_args(self):
        return [
            self.define_from_variant("ICET_USE_OPENGL", "opengl"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Work-around for ill-placed CMake modules"""
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix.lib)
