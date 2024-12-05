# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tinyobjloader(CMakePackage):
    """Tiny but powerful single file wavefront obj loader."""

    homepage = "https://github.com/tinyobjloader/tinyobjloader"
    url = "https://github.com/tinyobjloader/tinyobjloader/archive/refs/tags/v1.0.6.tar.gz"

    license("MIT")

    version("1.0.6", sha256="19ee82cd201761954dd833de551edb570e33b320d6027e0d91455faf7cd4c341")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.11:", type="build")
