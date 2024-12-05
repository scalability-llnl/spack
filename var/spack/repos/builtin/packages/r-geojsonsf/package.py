# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeojsonsf(RPackage):
    """GeoJSON to Simple Feature Converter.

    Converts Between GeoJSON and simple feature objects."""

    cran = "geojsonsf"

    license("MIT")

    version("2.0.3", sha256="275ca14672d982e6a95884515f49d8a0aad14f3be62ea01b675a91b0bffb46d1")
    version("2.0.1", sha256="42df40433bfbece5a39cd97b5bd4690b4424855241fcc3e7322ee68a3988bfbf")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-geometries", type=("build", "run"))
    depends_on("r-jsonify@1.1.1:", type=("build", "run"))
    depends_on("r-rapidjsonr@1.2.0:", type=("build", "run"))
    depends_on("r-sfheaders@0.2.2:", type=("build", "run"))
