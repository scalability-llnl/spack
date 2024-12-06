# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOdcGeo(PythonPackage):
    """Geometry Classes and Operations (opendatacube)."""

    homepage = "https://github.com/opendatacube/odc-geo/"
    pypi = "odc-geo/odc-geo-0.1.2.tar.gz"

    license("Apache-2.0")

    version("0.1.2", sha256="c5ec3c66a326b138df5a28aa639b1c2c3c644093af463948255219bdc2513408")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@51:", type="build")
    depends_on("py-affine", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyproj", type=("build", "run"))
    depends_on("py-shapely", type=("build", "run"))
