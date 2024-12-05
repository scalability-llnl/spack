# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FoonathanMemory(CMakePackage):
    """STL compatible C++ memory allocator library using a new RawAllocator concept
    that is similar to an Allocator but easier to use and write."""

    homepage = "https://memory.foonathan.net/"
    url = "https://github.com/foonathan/memory/archive/v0.7.tar.gz"

    license("Zlib")

    version("0.7-3", sha256="4203d15db22a94a3978eeb1afb59a37d35c57c0f148733f0f1a53a6281cb74dd")
    version("0.7", sha256="01a7cc5a5ebddbd71bec69c89562a4a2ecd7c29334c0a29d38d83e7f7f66eb53")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.14:", when="@0.7-3:", type="build")
    depends_on("cmake@3.1:", type="build")
