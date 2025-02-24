# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgooglemaps(RPackage):
    """Overlays on Static Maps.

    This package serves two purposes: (i) Provide a comfortable R interface to
    query the Google server for static maps, and (ii) Use the map as a
    background image to overlay plots within R. This requires proper coordinate
    scaling."""

    cran = "RgoogleMaps"

    version("1.5.1", sha256="14fe6c37d935a1c5a9ac063c9c9c59a1e93c6f86907480792302f9a9452cf8a4")
    version("1.4.5.3", sha256="d1d5ad8db841754af175d4104a05c5c31e5cc445be314a3ac70483c31798680b")
    version("1.4.3", sha256="44cb62bcd23e5b4807e91c5825352eb8d38aaaeb3b38a8271ca9f21c1e1d4b19")
    version("1.4.2", sha256="b479996fcb72f067644a7ea7f00325e44e76efd202e84aaab022753c4a6d5584")
    version("1.2.0.7", sha256="9c268a5a554ad6da69fb560d88dea9c86ec9e9a56b691f1b63faedfe20826712")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-png", type=("build", "run"))

    depends_on("r-sp", type=("build", "run"), when="@1.4.5.3:1.4.5.3")
    depends_on("r-rjsonio", type=("build", "run"), when="@1.2.0.5:1.2.0.7")
