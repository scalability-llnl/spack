# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSftime(RPackage):
    """Classes and Methods for Simple Feature Objects that Have a Time Column.

    Classes and methods for spatial objects that have a registered time column,
    in particular for irregular spatiotemporal data. The time column can be of
    any type, but needs to be ordinal. Regularly laid out spatiotemporal data
    (vector or raster data cubes) are handled by package 'stars'."""

    cran = "sftime"

    version("0.2-0", sha256="d82a1d750fb0fe7fe9962e520f00f8f969fe075a9bb53592180b4ff41430b1fa")

    depends_on("r-sf@1.0.7:", type=("build", "run"))
