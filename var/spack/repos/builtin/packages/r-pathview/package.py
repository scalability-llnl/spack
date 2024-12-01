# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPathview(RPackage):
    """a tool set for pathway based data integration and visualization.

    Pathview is a tool set for pathway based data integration and
    visualization. It maps and renders a wide variety of biological data on
    relevant pathway graphs. All users need is to supply their data and
    specify the target pathway. Pathview automatically downloads the pathway
    graph data, parses the data file, maps user data to the pathway, and
    render pathway graph with the mapped data. In addition, Pathview also
    seamlessly integrates with pathway and gene set (enrichment) analysis
    tools for large-scale and fully automated analysis."""

    bioc = "pathview"

    version("1.40.0", commit="6546c6139f797bdff2fcc0645030a5de3588f2eb")
    version("1.38.0", commit="8229376ffd45278b74a6e4ccfb3abea8992667f7")
    version("1.36.1", commit="f2e86b106c1cd91aac703337f968b7593a61c68d")
    version("1.36.0", commit="4f6be090a4089b5259d8e796d62f9830e2d63943")
    version("1.34.0", commit="a8788902a3bb047f8ee785966e57f84596076bbd")
    version("1.30.1", commit="a6a32395db408798cb076894678e90148bae6bf4")
    version("1.24.0", commit="e4401c1425c980ce2e6e478a4602a9f6d36ccd8d")
    version("1.22.3", commit="ff86f9e166a5b03bbed1a0ad276778958c3045ce")
    version("1.20.0", commit="a195afa6ba6c7917af2c7f77170f0644c46880c7")
    version("1.18.2", commit="d2048981696564ec75f661ed665977d3a6e09188")
    version("1.16.7", commit="fc560ed15ef7393a73d35e714716cc24dc835339")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-kegggraph", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-rgraphviz", type=("build", "run"))
    depends_on("r-graph", type=("build", "run"))
    depends_on("r-png", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-org-hs-eg-db", type=("build", "run"))
    depends_on("r-keggrest", type=("build", "run"))
