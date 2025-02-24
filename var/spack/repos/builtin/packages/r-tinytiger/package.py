# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTinytiger(RPackage):
    """Lightweight Interface to TIGER/Line Shapefiles

    Download geographic shapes from the United States Census Bureau TIGER/Line
    Shapefiles
    <https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html>.
    Functions support downloading and reading in geographic boundary data. All
    downloads can be set up with a cache to avoid multiple downloads. Data is
    available back to 2000 for most geographies."""

    homepage = "https://alarm-redist.org/tinytiger/"
    cran = "tinytiger"

    maintainers("jgaeb")

    license("MIT")

    version("0.0.9", sha256="fe9b1098a2d1d4722f8a7657a9244afcd3d6b7f4f112fc6a92c2fb75da07de59")
    version("0.0.4", sha256="818328b5095d9e8b302f1a04d004cd3ec6e62d945dbd757fe15e9ab768a7459e")
    version("0.0.3", sha256="841d92dd4185b9bff5eef0d3635805c5a3efb1bc4ff0a1101ef264417e37921c")

    depends_on("r@2.0.0:", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"), when="@0.0.4:")
    depends_on("r-cli")
    depends_on("r-glue")
    depends_on("r-curl")
    depends_on("r-sf")

    depends_on("r-rlang", type=("build", "run"), when="@:0.0.8")
