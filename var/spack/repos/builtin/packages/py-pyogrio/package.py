# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyogrio(PythonPackage):
    """Vectorized spatial vector file format I/O using GDAL/OGR"""

    homepage = "https://pypi.org/project/pyogrio"
    pypi = "pyogrio/pyogrio-0.9.0.tar.gz"
    git = "https://github.com/geopandas/pyogrio.git"

    maintainers("climbfuji")

    license("MIT", checked_by="climbfuji")

    version("0.9.0", sha256="6a6fa2e8cf95b3d4a7c0fac48bce6e5037579e28d3eb33b53349d6e11f15e5a8")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("gdal@2.4:", type=("build", "link", "run"))
    depends_on("py-cython@0.29:", type="build")
    depends_on("py-versioneer@0.28 +toml", type="build")
    # this is an implicit dependency already listed in py-versioneer, not needed
    # depends_on("py-tomli", when="^python@:3.10", type="build")

    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
