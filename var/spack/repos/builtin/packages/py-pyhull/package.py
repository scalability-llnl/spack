# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyhull(PythonPackage):
    """Pyhull is a Python wrapper to Qhull (http://www.qhull.org/) for the
    computation of the convex hull, Delaunay triangulation and Voronoi diagram.
    It is written as a Python C extension, with both high-level and low-level
    interfaces to qhull."""

    homepage = "https://github.com/materialsvirtuallab/pyhull"
    pypi = "pyhull/pyhull-2015.2.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("2015.2.1", sha256="d2ff0aa3298b548287587609a24f4e2aae7f7b8b1df152a90cd313260abc3a24")

    depends_on("c", type="build")  # generated

    # From setup.py:
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
