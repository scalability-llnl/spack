# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# ----------------------------------------------------------------------------


class RLeafpop(RPackage):
    """Include Tables, Images and Graphs in Leaflet Pop-Ups.

    Creates 'HTML' strings to embed tables, images or graphs in pop-ups of
    interactive maps created with packages like 'leaflet' or 'mapview'. Handles
    local images located on the file system or via remote URL. Handles graphs
    created with 'lattice' or 'ggplot2' as well as interactive plots created
    with 'htmlwidgets'."""

    cran = "leafpop"

    license("MIT")

    version("0.1.0", sha256="6e546886e1db4ad93a038de6d1e8331c0d686e96a0d3f0694e7575471f7d9db1")
    version("0.0.6", sha256="3d9ca31d081ce8540a87790786840bde5f833543af608c53a26623c7874e722f")

    depends_on("r-base64enc", type=("build", "run"))
    depends_on("r-brew", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-svglite", type=("build", "run"))
    depends_on("r-uuid", type=("build", "run"))
