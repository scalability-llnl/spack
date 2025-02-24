# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgplotify(RPackage):
    """Convert Plot to 'grob' or 'ggplot' Object.

    Convert plot function call (using expression or formula) to 'grob' or
    'ggplot' object that compatible to the 'grid' and 'ggplot2' ecosystem. With
    this package, we are able to e.g. using 'cowplot' to align plots produced
    by 'base' graphics, 'ComplexHeatmap', 'eulerr', 'grid', 'lattice',
    'magick', 'pheatmap', 'vcd' etc. by converting them to 'ggplot' objects."""

    cran = "ggplotify"

    license("Artistic-2.0")

    version("0.1.2", sha256="01bae5759e14e211bddb04413e094ba31399b513989894ea08602d202f990e87")
    version("0.1.0", sha256="178f73d6d3dc391c3efb1a62c95fe38587044f9e3288dffb915d3687941bb38a")
    version("0.0.5", sha256="035ea6a70023c4819c8a486d0fd94c2765aa4d6df318747e104eeb9829b9d65d")
    version("0.0.3", sha256="7e7953a2933aa7127a0bac54375e3e0219a0744cfc3249c3d7b76065f7a51892")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-gridgraphics", type=("build", "run"))
    depends_on("r-yulab-utils", type=("build", "run"), when="@0.1.0:")

    depends_on("r-rvcheck", type=("build", "run"), when="@:0.0.5")
