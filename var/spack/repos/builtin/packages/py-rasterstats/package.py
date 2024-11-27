# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRasterstats(PythonPackage):
    """rasterstats is a Python module for summarizing geospatial raster datasets
    based on vector geometries. It includes functions for zonal statistics and
    interpolated point queries. The command-line interface allows for easy
    interperability with other GeoJSON tools."""

    homepage = "https://github.com/perrygeo/python-rasterstats"
    pypi = "rasterstats/rasterstats-0.17.0.tar.gz"

    license("BSD-3-Clause")

    version("0.17.0", sha256="27975ebc0a402865dd9e92ad4ecf0dd62678e320735cc81e104c730e6d001298")

    depends_on("py-affine@:2", type=("build", "run"))
    depends_on("py-shapely", type=("build", "run"))
    depends_on("py-numpy@1.9:", type=("build", "run"))
    depends_on("py-rasterio@1.0:", type=("build", "run"))
    depends_on("py-cligj@0.4:", type=("build", "run"))
    depends_on("py-fiona", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
