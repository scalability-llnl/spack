# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgexf(RPackage):
    """Create, read and write GEXF (Graph Exchange XML Format) graph files
    (used in Gephi and others). Using the XML package, it allows the user to
    easily build/read graph files including attributes, GEXF viz attributes
    (such as color, size, and position), network dynamics (for both edges and
    nodes) and edge weighting. Users can build/handle graphs element-by-element
    or massively through data-frames, visualize the graph on a web browser
    through "sigmajs" (a javascript library) and interact with the igraph
    package."""

    homepage = "http://bitbucket.org/gvegayon/rgexf"
    url      = "https://cloud.r-project.org/src/contrib/rgexf_0.15.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rgexf"

    version('0.15.3', sha256='2e8a7978d1fb977318e6310ba65b70a9c8890185c819a7951ac23425c6dc8147')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rook', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
