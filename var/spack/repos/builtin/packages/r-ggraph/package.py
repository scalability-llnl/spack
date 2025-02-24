# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgraph(RPackage):
    """An Implementation of Grammar of Graphics for Graphs and Networks.

    The grammar of graphics as implemented in ggplot2 is a poor fit for graph
    and network visualizations due to its reliance on tabular data input.
    ggraph is an extension of the ggplot2 API tailored to graph visualizations
    and provides the same flexible approach to building up plots layer by
    layer."""

    cran = "ggraph"

    license("MIT")

    version("2.2.1", sha256="4405f8a907ad8fee68b5d4991f0bc8f35d6c0facbb7467c2ce425d3ec8b23af1")
    version("2.1.0", sha256="686fdb22dc4f613273fb755ec42399a208b4d10348eecd1a217afd4612245c1f")
    version("2.0.6", sha256="7b0ac90d834a3ce5641b4bca159d59d09607ddaab592908361b75cffb648d40a")
    version("2.0.5", sha256="e36ad49dba92ee8652e18b1fb197be0ceb9f0a2f8faee2194453a62578449654")
    version("2.0.4", sha256="9c6092d9a98b7b116f9c765ba44de7a34ceff2f584e776ef7a2082ad1d717dc8")
    version("2.0.0", sha256="4307efe85bfc6a0496797f6b86d6b174ba196538c51b1a6b6af55de0d4e04762")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.5.0:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-ggforce@0.3.1:", type=("build", "run"))
    depends_on("r-igraph@1.0.0:", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-ggrepel", type=("build", "run"))
    depends_on("r-viridis", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-tidygraph", type=("build", "run"))
    depends_on("r-graphlayouts@0.5.0:", type=("build", "run"))
    depends_on("r-graphlayouts@1.1.0:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-withr", type=("build", "run"), when="@2.0.4:")
    depends_on("r-lifecycle", type=("build", "run"), when="@2.1.0:")
    depends_on("r-memoise", type=("build", "run"), when="@2.2.0:")
    depends_on("r-vctrs", type=("build", "run"), when="@2.1.0:")
    depends_on("r-cli", type=("build", "run"), when="@2.1.0:")
    depends_on("r-cpp11", type=("build", "run"), when="@2.2.0:")

    depends_on("r-rcpp@0.12.2:", type=("build", "run"), when="@:2.1.0")
    depends_on("r-digest", type=("build", "run"), when="@:2.1.0")
    depends_on("r-gtable", type=("build", "run"), when="@:2.1.0")
