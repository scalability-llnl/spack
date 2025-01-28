# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLeafem(RPackage):
    """'leaflet' Extensions for 'mapview'.

    Provides extensions for packages 'leaflet' & 'mapdeck', many of which are
    used by package 'mapview'. Focus is on functionality readily available in
    Geographic Information Systems such as 'Quantum GIS'. Includes functions to
    display coordinates of mouse pointer position, query image values via mouse
    pointer and zoom-to-layer buttons. Additionally, provides a feature type
    agnostic function to add points, lines, polygons to a map."""

    cran = "leafem"

    license("MIT")

    version("0.2.3", sha256="defd5baa4383da4182e97d41145c7a9633a987de05c465eb99a7a452fbf375e3")
    version("0.2.0", sha256="97eb78b3eaf6012940f2c4f73effd8ff2d39aa46fef5f2ddf0005990b07dba8d")
    version("0.1.6", sha256="ca50e0a699f564449248511857a2df0d48cd07de3157e099478a19b533088156")
    version("0.1.3", sha256="6f123fc15efadb85d317c01003e3b7af5dc925cffe0bbe774b1b39b6bd67f304")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"))
    depends_on("r-geojsonsf", type=("build", "run"), when="@0.1.6:")
    depends_on("r-htmltools@0.3:", type=("build", "run"))
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-leaflet@2.0.1:", type=("build", "run"))
    depends_on("r-raster", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-png", type=("build", "run"))
