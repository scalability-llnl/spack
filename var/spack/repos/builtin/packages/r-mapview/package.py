# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMapview(RPackage):
    """Interactive Viewing of Spatial Data in R.

    Quickly and conveniently create interactive visualisations of spatial data
    with or without background maps. Attributes of displayed features are fully
    queryable via pop-up windows. Additional functionality includes methods to
    visualise true- and false-color raster images and bounding boxes."""

    cran = "mapview"

    license("GPL-3.0-or-later OR custom")

    version("2.11.2", sha256="414d7f732b3aaf62005e279d7b0febf50aed2183bf05522c4fccaa92117328b0")
    version("2.11.0", sha256="87f8cf562a0918201082a743438b9af47429bdb8871511235d72505107f4d30a")
    version("2.10.0", sha256="b597902c654b9abf1163bb9d4f1044fef85d0a52c8dc6538ca46b0024f63baaa")
    version("2.9.0", sha256="170cb2b5e67cbeb177f87bd2eab1ecabc44a1042addbcd95a85b2ec4a00eb690")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-leafem", type=("build", "run"))
    depends_on("r-leaflet@2.0.0:", type=("build", "run"))
    depends_on("r-leafpop", type=("build", "run"))
    depends_on("r-png", type=("build", "run"))
    depends_on("r-raster", type=("build", "run"))
    depends_on("r-raster@3.6.3:", type=("build", "run"), when="@2.11.2:")
    depends_on("r-satellite", type=("build", "run"))
    depends_on("r-scales@0.2.5:", type=("build", "run"))
    depends_on("r-servr", type=("build", "run"), when="@2.10.0:")
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
    depends_on("gmake", type="build")

    depends_on("r-webshot", type=("build", "run"), when="@:2.11.0")
