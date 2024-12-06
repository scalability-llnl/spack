# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGdalutils(RPackage):
    """Wrappers for the Geospatial Data Abstraction Library (GDAL)
    Utilities."""

    cran = "gdalUtils"

    version("2.0.3.2", sha256="4c6faabee2db8a87b7ea0f8e67e9fce3c5db7f4be353d7d86ea559507cbb2a4f")
    version("2.0.1.14", sha256="890a502b2eb5f1b23655fab94caad5d32adca05b93f5db1d96d9dcde3f0e7737")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))
    depends_on("r-raster", type=("build", "run"))
    depends_on("r-rgdal", type=("build", "run"))
    depends_on("gdal")
