# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIsoband(RPackage):
    """Generate Isolines and Isobands from Regularly Spaced Elevation Grids.

    A fast C++ implementation to generate contour lines (isolines) and contour
    polygons (isobands) from regularly spaced grids containing elevation
    data."""

    cran = "isoband"

    license("MIT")

    version("0.2.7", sha256="7693223343b45b86de2b5b638ff148f0dafa6d7b1237e822c5272902f79cdf61")
    version("0.2.6", sha256="27e460945753f6710649563dc817e2f314392ef6d1f8b6af2b1bf9447fab43a3")
    version("0.2.5", sha256="46f53fa066f0966f02cb2bf050190c0d5e950dab2cdf565feb63fc092c886ba5")
    version("0.2.3", sha256="f9d3318fdf6d147dc2e2c7015ea7de42a55fa33d6232b952f982df96066b7ffe")

    depends_on("cxx", type="build")  # generated

    depends_on("r-testthat", type=("build", "run"), when="@0.2.3")
