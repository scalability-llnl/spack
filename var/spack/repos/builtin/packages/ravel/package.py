# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ravel(CMakePackage):
    """Ravel is a parallel communication trace visualization tool that
    orders events according to logical time."""

    homepage = "https://github.com/llnl/ravel"
    url = "https://github.com/llnl/ravel/archive/v1.0.0.tar.gz"

    version("1.0.0", sha256="e1e1ac6d70c9aae915623d81a8f1258488fd26f880612fe21f2e032827aa93eb")

    depends_on("cxx", type="build")  # generated
    # See https://github.com/LLNL/ravel/pull/18
    patch("qpainterpath.patch")

    depends_on("cmake@2.8.9:", type="build")

    depends_on("muster@1.0.1:")
    depends_on("otf")
    depends_on("otf2")
    depends_on("qt@5:+opengl")

    def cmake_args(self):
        return ["-Wno-dev"]
