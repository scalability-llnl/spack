# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RExactextractr(RPackage):
    """Fast Extraction from Raster Datasets using Polygons.

    Provides a replacement for the 'extract' function from the 'raster' package
    that is suitable for extracting raster values using 'sf' polygons."""

    cran = "exactextractr"

    license("Apache-2.0")

    version("0.10.0", sha256="9b7fc3c6f0e9e89596a1992240ecbb8e2893f4addffaecbd852403c10a0943de")
    version("0.9.1", sha256="f0cf367c25a45b09eda1d435c8c818590ff4de86162f675e3172821d1853f4a1")
    version("0.9.0", sha256="705a355534f427dc832af2a294aaf928c10c72d6335d38aed86da64d814eb18d")
    version("0.8.2", sha256="cc32ab3af8d881a7e7836c296ea42f3fdabf3373ec1de0b154dbfe9870ee8a74")
    version("0.7.2", sha256="2eb2b5eb2156cca875e7004b80687589217abd6fce5ebb7d8acb7fa71f6e6958")
    version("0.5.1", sha256="47ddfb4b9e42e86957e03b1c745d657978d7c4bed12ed3aa053e1bc89f20616d")
    version("0.3.0", sha256="c7fb38b38b9dc8b3ca5b8f1f84f4ba3256efd331f2b4636b496d42689ffc3fb0")
    version("0.2.1", sha256="d0b998c77c3fd9265a600a0e08e9bf32a2490a06c19df0d0c0dea4b5c9ab5773")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.12:", type=("build", "run"))
    depends_on("r-raster", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-sf@0.9.0:", type=("build", "run"), when="@0.7.2:")
    depends_on("geos@3.5.0:")
