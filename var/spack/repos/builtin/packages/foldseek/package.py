# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Foldseek(CMakePackage):
    """Foldseek enables fast and sensitive comparisons of large protein structure sets"""

    homepage = "https://foldseek.com/"
    url = "https://github.com/steineggerlab/foldseek/archive/refs/tags/8-ef4e960.tar.gz"

    license("GPL-3.0-only", checked_by="A-N-Other")

    version("9-427df8a", sha256="b17d2d85b49a8508f79ffd8b15e54afc5feef5f3fb0276a291141ca5dbbbe8bc")
    version("8-ef4e960", sha256="c74d02c4924d20275cc567783b56fff10e76ed67f3d642f53c283f67c4180a1e")
    version("7-04e0ec8", sha256="009d722d600248a680b9e1e9dcb3bf799f8be8de41e80a598b7f39a5ced54191")

    depends_on("zlib-api")
    depends_on("bzip2")
    depends_on("openmpi")
    depends_on("rust", type="build")
    depends_on("rust@1.78.0", when="@:9", type="build")
