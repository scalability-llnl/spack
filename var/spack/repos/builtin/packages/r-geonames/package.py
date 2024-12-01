# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeonames(RPackage):
    """Interface to the "Geonames" Spatial Query Web Service.

    The web service at <https://www.geonames.org/> provides a number of spatial
    data queries, including administrative area hierarchies, city locations and
    some country postal code queries. A (free) username is required and rate
    limits exist."""

    cran = "geonames"

    license("GPL-3.0-only")

    version("0.999", sha256="1dd7bbd82d9425d14eb36f8e5bf431feaccfe3b0c4e70bf38f44f13dfc59e17b")

    depends_on("r@2.2.0:", type=("build", "run"))
    depends_on("r-rjson", type=("build", "run"))
