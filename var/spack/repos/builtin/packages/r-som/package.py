# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSom(RPackage):
    """Self-Organizing Map.

    Self-Organizing Map (with application in gene clustering)."""

    cran = "som"

    license("GPL-3.0-or-later")

    version("0.3-5.1", sha256="a6f4c0e5b36656b7a8ea144b057e3d7642a8b71972da387a7133f3dd65507fb9")
    version("0.3-5", sha256="f7672afaaffcf41a8b2dd50e4c76b3a640ea2ad099f18b5dfcf00389abf6ba07")
    version("0.3-4", sha256="679e3d3f0af6e56da3b0a4d8577334e03ad45fe76916bbc2592548f85b6b1c84")
    version("0.3-3", sha256="434e2210df3e6a459a8588606676c02494f58c5b52e25291d142121b7b9be5c7")
    version("0.3-2", sha256="b46ecb79c08f3d4cf9527d5c7f85a235808dda45dae7f50909b2df90e7b9e543")

    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
