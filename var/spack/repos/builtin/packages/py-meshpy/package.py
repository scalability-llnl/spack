# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMeshpy(PythonPackage):
    """Simplicial Mesh Generation from Python"""

    homepage = "https://documen.tician.de/meshpy/"
    pypi = "MeshPy/MeshPy-2022.1.3.tar.gz"
    git = "https://github.com/inducer/meshpy.git"

    maintainers("cgcgcg")

    license("MIT")

    version("2022.1.3", sha256="a7158e31ece25fa6c6cebce9fd1e968157d661dc8769fb30ceba69c351478475")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", type="build")
    depends_on("py-pytools@2011.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-gmsh-interop", type=("build", "run"))
