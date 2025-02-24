# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeocube(PythonPackage):
    """Tool to convert geopandas vector data into rasterized xarray data."""

    homepage = "https://github.com/corteva/geocube"
    pypi = "geocube/geocube-0.0.17.tar.gz"

    license("BSD-3-Clause")
    maintainers("adamjstewart")

    version("0.7.0", sha256="986ff46e78d7dede09a1c93bff1642c24aaa5590acdc774049436f86f0989ca4")
    version("0.3.2", sha256="71ff0228f1ef44e3a649d29a045ff7e2a2094a5cfca30fadab8f88f4ec23a41d")
    version("0.3.1", sha256="5c97131010cd8d556a5fad2a3824452120640ac33a6a45b6ca9ee3c28f2e266f")
    version("0.0.17", sha256="bf8da0fa96d772ebaea0b98bafa0ba5b8639669d5feb07465d4255af177bddc0")

    depends_on("python@3.10:", when="@0.4.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-click@6.0:", type=("build", "run"))
    depends_on("py-geopandas@1:", when="@0.6:", type=("build", "run"))
    depends_on("py-geopandas@0.7:", type=("build", "run"))
    depends_on("py-odc-geo", when="@0.2:", type=("build", "run"))
    depends_on("py-rasterio@1.3:", when="@0.4.3:", type=("build", "run"))
    depends_on("py-rasterio", type=("build", "run"))
    depends_on("py-rioxarray@0.4:", type=("build", "run"))
    depends_on("py-scipy", when="@0.0.18:", type=("build", "run"))
    depends_on("py-xarray@0.17:", type=("build", "run"))
    depends_on("py-pyproj@2:", type=("build", "run"))
    depends_on("py-numpy@1.20:", when="@0.3:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-datacube", when="@:0.1", type=("build", "run"))
