# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDiagrammer(RPackage):
    """Graph/Network Visualization.

    Build graph/network structures using functions for stepwise addition and
    deletion of nodes and edges. Work with data available in tables for bulk
    addition of nodes, edges, and associated metadata. Use graph selections and
    traversals to apply changes to specific nodes or edges. A wide selection of
    graph algorithms allow for the analysis of graphs. Visualize the graphs and
    take advantage of any aesthetic properties assigned to nodes and edges."""

    cran = "DiagrammeR"

    version("1.0.11", sha256="e873e3d6e198232408161661001ddcb04c9a56065bb4703c925e538462f4c4df")
    version("1.0.9", sha256="64a426fe27110dddd8b0c1223ae4c397a2e553ae5e81ddd4ff67c026cfc40abf")
    version("1.0.8", sha256="b9157b26215edda4fe0a1b9330a597d5b01a5d7e660a9832f593b87c584dd233")
    version("1.0.7", sha256="6af291a7136657b9f7c67b96cd7f3afe99662cf5a477ebbb213a6c53df623050")
    version("1.0.6.1", sha256="be4e4c520a3692902ce405e8225aef9f3d5f0cd11fcde614f6541e981b63673d")
    version("1.0.1", sha256="ccee8acf608fc909e73c6de4374cef5a570cb62e5f454ac55dda736f22f3f013")
    version("1.0.0", sha256="2b186dae1b19018681b979e9444bf16559c42740d8382676fbaf3b0f8a44337e")
    version("0.8.4", sha256="0503935fa120c7c7cdcfd4dce85558b23fd0bcb7e6b32fa6989087d3c88ec404")

    depends_on("r@3.2.0:", type=("build", "run"), when="@0.9.2:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.0.7")
    depends_on("r-cli", type=("build", "run"), when="@1.0.11:")
    depends_on("r-dplyr@0.7.4:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-dplyr@0.7.6:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-dplyr@1.0.7:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-glue@1.2.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-glue@1.3.0:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-glue@1.5.0:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-htmltools@0.3.6:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-htmltools@0.5.2:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-htmlwidgets@1.0:", type=("build", "run"))
    depends_on("r-htmlwidgets@1.2:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-htmlwidgets@1.5:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-igraph@1.1.2:", type=("build", "run"))
    depends_on("r-igraph@1.2.2:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-igraph@1.2.11:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-igraph@1.4.0:", type=("build", "run"), when="@1.0.11:")
    depends_on("r-magrittr@1.5:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-purrr@0.2.4:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-purrr@0.2.5:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-purrr@0.3.4:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-rcolorbrewer@1.1-2:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-readr@1.1.1:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-readr@2.1.1:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-rlang@0.2.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rlang@0.2.2:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-rlang@0.4:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.0.11:")
    depends_on("r-rstudioapi@0.7:", type=("build", "run"))
    depends_on("r-scales@0.5.0:", type=("build", "run"))
    depends_on("r-scales@1.0.0:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-scales@1.1:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-stringr@1.3.0:", type=("build", "run"))
    depends_on("r-stringr@1.3.1:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-stringr@1.4:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-tibble@1.4.2:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-tibble@3.1:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-tidyr@0.8.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-tidyr@0.8.1:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-tidyr@1.1:", type=("build", "run"), when="@1.0.7:")
    depends_on("r-viridislite@0.4.2:", type=("build", "run"), when="@1.0.11:")
    depends_on("r-visnetwork@2.0.3:", type=("build", "run"))
    depends_on("r-visnetwork@2.0.4:", type=("build", "run"), when="@1.0.6.1:")
    depends_on("r-visnetwork@2.1.0:", type=("build", "run"), when="@1.0.7:")

    depends_on("r-downloader@0.4:", type=("build", "run"), when="@1.0.0:1.0.10")
    depends_on("r-influencer@0.1.0:", type=("build", "run"), when="@:1.0.9")
    depends_on("r-influencer@0.1.0.1:", type=("build", "run"), when="@1.0.7:1.0.9")
    depends_on("r-viridis@0.5.0:", type=("build", "run"), when="@1.0.0:1.0.10")
    depends_on("r-viridis@0.5.1:", type=("build", "run"), when="@1.0.6.1:1.0.10")
    depends_on("r-viridis@0.6.2:", type=("build", "run"), when="@1.0.7:1.0.10")
    depends_on("r-rgexf@0.15.3:", type=("build", "run"), when="@1.0.0:1.0.1")
