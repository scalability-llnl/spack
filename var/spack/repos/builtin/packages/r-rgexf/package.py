# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgexf(RPackage):
    """Build, Import and Export GEXF Graph Files.

    Create, read and write GEXF (Graph Exchange XML Format) graph files (used
    in Gephi and others). Using the XML package, it allows the user to easily
    build/read graph files including attributes, GEXF viz attributes (such as
    color, size, and position), network dynamics (for both edges and nodes) and
    edge weighting. Users can build/handle graphs element-by-element or
    massively through data-frames, visualize the graph on a web browser through
    "sigmajs" (a javascript library) and interact with the igraph package."""

    cran = "rgexf"

    license("MIT")

    version("0.16.3", sha256="cddcc58a10092cfea32999d7baaf6eae9b34e649a16627ee0b466a7cf2c339b0")
    version("0.16.2", sha256="6ee052b0de99d0c7492366b991d345a51b3d0cc890d10a68b8670e1bd4fc8201")
    version("0.16.0", sha256="2a671df9ac70cfefd4092754317cb28e32a33df345b80e1975bf838e838245ee")
    version("0.15.3", sha256="2e8a7978d1fb977318e6310ba65b70a9c8890185c819a7951ac23425c6dc8147")

    depends_on("r-xml", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-servr", type=("build", "run"), when="@0.16.0:")

    depends_on("r-rook", type=("build", "run"), when="@:0.15.3")
