# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKegggraph(RPackage):
    """KEGGgraph: A graph approach to KEGG PATHWAY in R and Bioconductor.

    KEGGGraph is an interface between KEGG pathway and graph object as well
    as a collection of tools to analyze, dissect and visualize these graphs.
    It parses the regularly updated KGML (KEGG XML) files into graph models
    maintaining all essential pathway attributes. The package offers
    functionalities including parsing, graph operation, visualization and
    etc."""

    bioc = "KEGGgraph"

    version("1.60.0", commit="9fc1e371309193e7ff47b0e9d9937cbeed830a1c")
    version("1.58.0", commit="7c3f148b57903b8df517f94824f07f38bbd3b591")
    version("1.56.0", commit="e95cbf9f8a095d59b78a053463191b89c00d5ded")
    version("1.54.0", commit="135ee3dad30ca208e21acd0a2d81120b74b64079")
    version("1.50.0", commit="3335e85cdba264c04e6e36378578cf6c83a30eb8")
    version("1.44.0", commit="2c24e8ec53fe34c72ea65f34e3c09905ab2e5c62")
    version("1.42.0", commit="7d907e22a3ad7b4829a7cbaba5a8f8dc8013a609")
    version("1.40.0", commit="6351a1637276f71697b01a994ebda0d3d1cf6d7a")
    version("1.38.0", commit="72f102e2611e3966362cfaa43646a6e66dd2ba27")
    version("1.38.1", commit="dd31665beb36d5aad8ed09ed56c603633b6b2292")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.54.0:")
    depends_on("r-xml@2.3-0:", type=("build", "run"))
    depends_on("r-graph", type=("build", "run"))
    depends_on("r-rcurl", type=("build", "run"), when="@1.44.0:")
    depends_on("r-rgraphviz", type=("build", "run"), when="@1.54.0:")
