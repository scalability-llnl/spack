# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRegionmask(PythonPackage):
    """Create masks of geospatial regions for arbitrary grids"""

    homepage = "https://pypi.org/project/regionmask"
    pypi = "regionmask/regionmask-0.12.1.tar.gz"
    git = "https://github.com/regionmask/regionmask.git"

    maintainers("climbfuji")

    license("MIT", checked_by="climbfuji")

    version("0.12.1", sha256="7ef1e70c6ebab7bfc6a80e13f6fe771945b8b6a31b7f8980fc88c8b8505bb854")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@7:", type="build")

    depends_on("py-geopandas@0.13:", type=("build", "run"))
    depends_on("py-numpy@1.24:", type=("build", "run"))
    depends_on("py-packaging@23.1:", type=("build", "run"))
    depends_on("py-pooch@1.7:", type=("build", "run"))
    depends_on("py-rasterio@1.3:", type=("build", "run"))
    depends_on("py-shapely@2.0:", type=("build", "run"))
    depends_on("py-xarray@2023.7:", type=("build", "run"))

    # "Optional" dependencies for plotting, but that's what this package is really useful for
    depends_on("py-matplotlib@3.7:", type="run")
    depends_on("py-cartopy@0.22:", type="run")
