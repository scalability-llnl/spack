# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBfastspatial(RPackage):
    """Pre-process gridded time-series data in order for them to be
    analyzed with change detection algorithms such as bfast. Uses classes
    from the raster package and includes utilities to run the algorithms and
    post-process the results."""

    homepage = "https://github.com/loicdtx/bfastSpatial"
    url = "https://github.com/loicdtx/bfastSpatial/archive/0.6.2.tar.gz"

    version("0.6.2", sha256="2c6220a5d04d6e4531b0b022a015651e630433f8d6864fa8b820aed5af5c1897")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-raster", type=("build", "run"))
    depends_on("r-bfast", type=("build", "run"))
    depends_on("r-gdalutils", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-rgdal", type=("build", "run"))
    depends_on("r-bitops", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
