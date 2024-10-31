# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brunsli(CMakePackage):
    """Brunsli is a lossless JPEG repacking library."""

    homepage = "https://github.com/google/brunsli"
    git = "https://github.com/google/brunsli.git"

    license("MIT")

    version("0.1", tag="v0.1", commit="8a0e9b8ca2e3e089731c95a1da7ce8a3180e667c", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")

    @property
    def libs(self):
        return find_libraries(
            ["libbrunslidec-c", "libbrunslienc-c"], root=self.prefix, recursive=True
        )
