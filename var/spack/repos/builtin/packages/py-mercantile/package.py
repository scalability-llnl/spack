# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMercantile(PythonPackage):
    """Web mercator XYZ tile utilities."""

    homepage = "https://github.com/mapbox/mercantile"
    pypi = "mercantile/mercantile-1.1.6.tar.gz"

    maintainers("adamjstewart")

    version("1.1.6", sha256="0dff4cbc2c92ceca0e0dfbb3dc74392a96d33cfa29afb1bdfcc80283d3ef4207")

    depends_on("py-setuptools", type="build")
    depends_on("py-click@3.0:", type=("build", "run"))
