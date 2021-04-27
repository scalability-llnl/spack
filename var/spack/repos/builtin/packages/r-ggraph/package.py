# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGgraph(RPackage):
    """An Implementation of Grammar of Graphics for Graphs and Networks

    The grammar of graphics as implemented in ggplot2 is a poor fit for graph
    and network visualizations due to its reliance on tabular data input.
    ggraph is an extension of the ggplot2 API tailored to graph visualizations
    and provides the same flexible approach to building up plots layer by
    layer."""

    homepage = "https://github.com/thomasp85/ggraph"
    url      = "https://cloud.r-project.org/src/contrib/ggraph_2.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggraph"

    version('2.0.4', sha256='9c6092d9a98b7b116f9c765ba44de7a34ceff2f584e776ef7a2082ad1d717dc8')
    version('2.0.0', sha256='4307efe85bfc6a0496797f6b86d6b174ba196538c51b1a6b6af55de0d4e04762')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.2:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-ggforce@0.3.1:', type=('build', 'run'))
    depends_on('r-igraph@1.0.0:', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
    depends_on('r-viridis', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-tidygraph', type=('build', 'run'))
    depends_on('r-graphlayouts@0.5.0:', type=('build', 'run'))
    depends_on('r-withr', when='@2.0.4:', type=('build', 'run'))
