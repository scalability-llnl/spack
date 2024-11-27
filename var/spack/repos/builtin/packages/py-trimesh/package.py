# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrimesh(PythonPackage):
    """Import, export, process, analyze and view triangular meshes"""

    homepage = "https://github.com/mikedh/trimesh"
    pypi = "trimesh/trimesh-2.38.10.tar.gz"

    license("MIT")

    version("3.17.1", sha256="025bb2fa3a2e87bdd6873f11db45a7ca19216f2f8b6aed29140fca57e32c298e")
    version("2.38.10", sha256="866e73ea35641ff2af73867c891d7f9b90c75ccb8a3c1e8e06e16ff9af1f8c64")

    variant(
        "easy",
        default=False,
        description="Install soft dependencies and unlock extra functionality",
    )

    depends_on("py-setuptools@40.8:", type="build")

    depends_on("py-chardet", type=("build", "run"), when="+easy")
    depends_on("py-colorlog", type=("build", "run"), when="+easy")
    depends_on("py-jsonschema", type=("build", "run"), when="+easy")
    depends_on("py-lxml", type=("build", "run"), when="+easy")
    depends_on("py-mapbox-earcut", type=("build", "run"), when="+easy")
    depends_on("py-msgpack", type=("build", "run"), when="+easy")
    depends_on("py-networkx", type=("build", "run"), when="+easy")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("pil", type=("build", "run"), when="+easy")
    depends_on("py-pycollada", type=("build", "run"), when="+easy")
    depends_on("py-pyglet@:1", type=("build", "run"), when="+easy")
    depends_on("py-requests", type=("build", "run"), when="+easy")
    depends_on("py-rtree", type=("build", "run"), when="+easy")
    depends_on("py-scipy", type=("build", "run"), when="+easy")
    depends_on("py-setuptools", type=("build", "run"), when="+easy")
    depends_on("py-shapely", type=("build", "run"), when="+easy")
    depends_on("py-svgpath", type=("build", "run"), when="+easy")
    depends_on("py-sympy", type=("build", "run"), when="+easy")
    depends_on("py-xxhash", type=("build", "run"), when="+easy")
