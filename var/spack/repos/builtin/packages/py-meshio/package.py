# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMeshio(PythonPackage):
    """MeshIO is a Python library to read and write many mesh formats."""

    homepage = "https://github.com/nschloe/meshio"
    pypi = "meshio/meshio-5.0.0.tar.gz"

    license("MIT")

    version("5.0.1", sha256="e283f40b5fb68fc5c232829c33c086789661438960762b22dc2823571a089a8b")
    version("5.0.0", sha256="f6327c06d6171d30e0991d3dcb048751035f9cfac1f19e2444971275fd971188")
    version("4.4.6", sha256="be352a0924c9eff99768a6f402b7558dbb280bbf1e7bf43f18cef92db418684f")

    depends_on("python@3.7:", when="@5.0.0:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
