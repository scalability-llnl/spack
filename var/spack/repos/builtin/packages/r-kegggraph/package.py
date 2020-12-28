# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://bioconductor.org/packages/KEGGgraph"
    git      = "https://git.bioconductor.org/packages/KEGGgraph.git"

    version('1.44.0', commit='2c24e8ec53fe34c72ea65f34e3c09905ab2e5c62')
    version('1.42.0', commit='7d907e22a3ad7b4829a7cbaba5a8f8dc8013a609')
    version('1.40.0', commit='6351a1637276f71697b01a994ebda0d3d1cf6d7a')
    version('1.38.0', commit='72f102e2611e3966362cfaa43646a6e66dd2ba27')
    version('1.38.1', commit='dd31665beb36d5aad8ed09ed56c603633b6b2292')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-xml@2.3-0:', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))

    depends_on('r-rcurl', when='@1.44.0:', type=('build', 'run'))
