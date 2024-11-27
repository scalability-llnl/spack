# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sdl2Ttf(CMakePackage):
    """Simple DirectMedia Layer 2 TrueType Fonts library"""

    homepage = "https://www.libsdl.org/projects/SDL_ttf/"
    url = "https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.20.2.tar.gz"
    git = "https://github.com/libsdl-org/SDL_ttf.git"

    license("Zlib")

    version("2.20.2", sha256="9dc71ed93487521b107a2c4a9ca6bf43fb62f6bddd5c26b055e6b91418a22053")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("sdl2")

    maintainers("georgemalerbo", "amklinv")
