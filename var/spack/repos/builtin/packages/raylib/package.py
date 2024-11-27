# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Raylib(CMakePackage):
    """Simple and easy-to-use library for game development and multimedia applications"""

    homepage = "https://www.raylib.com/"
    url = "https://github.com/raysan5/raylib/archive/refs/tags/5.0.tar.gz"
    git = "https://github.com/raysan5/raylib.git"

    maintainers("georgemalerbo")

    license("Zlib", checked_by="georgemalerbo")

    version("5.0", sha256="98f049b9ea2a9c40a14e4e543eeea1a7ec3090ebdcd329c4ca2cf98bc9793482")

    depends_on("c", type="build")  # generated

    # The package includes an llvm variant, which is disabled by default to simplify the build.
    # If enabled, allows Mesa to utilize software-based OpenGL rendering on systems without a GPU.
    variant("llvm", default=False, description="Enables LLVM support in Mesa")

    depends_on("cmake@3.11:", type="build")
    depends_on("glfw", when="platform=linux")
    depends_on("glfw", when="platform=darwin")
    depends_on("mesa", when="platform=linux +llvm")
    depends_on("mesa~llvm", when="platform=linux ~llvm")
    depends_on("mesa-glu", when="platform=linux")
