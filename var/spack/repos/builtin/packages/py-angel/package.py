# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAngel(PythonPackage):
    """ANGEL: Robust Open Reading Frame prediction"""

    homepage = "https://github.com/PacificBiosciences/ANGEL"
    url = "https://github.com/PacificBiosciences/ANGEL/archive/v3.0.tar.gz"

    license("MIT")

    version("3.0", sha256="a0319553055d3dfc84a4f732ed246c180c23ee9c397810c96acd7940721ae57d")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))

    depends_on("py-biopython@:1.72", type=("build", "run"))
