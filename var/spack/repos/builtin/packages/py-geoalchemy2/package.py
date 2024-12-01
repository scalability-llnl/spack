# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeoalchemy2(PythonPackage):
    """Using SQLAlchemy with Spatial Databases"""

    homepage = "https://geoalchemy-2.readthedocs.io/en/latest"
    pypi = "GeoAlchemy2/GeoAlchemy2-0.6.3.tar.gz"

    license("MIT")

    version("0.6.3", sha256="4dc4c6c2bda0fc82cccab4aaff185a6570e13a5351d85e29e12984a55d4138ee")
    version("0.4.2", sha256="17fa10b0c01bd2ab036ea56975dfa850098aa394a5d6ee04d88b2aefc16751cb")

    variant("dev", default=False, description="Enable development dependencies")

    depends_on("py-setuptools", type="build")
    depends_on("py-sqlalchemy@0.8:", type=("build", "run"))
    depends_on("py-shapely@1.3.0:", type=("build", "run"), when="+dev")
