# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://bioconductor.org/packages/pathview"
    git      = "https://git.bioconductor.org/packages/pathview.git"

    version('1.24.0', commit='e4401c1425c980ce2e6e478a4602a9f6d36ccd8d')
    version('1.22.3', commit='ff86f9e166a5b03bbed1a0ad276778958c3045ce')
    version('1.20.0', commit='a195afa6ba6c7917af2c7f77170f0644c46880c7')
    version('1.18.2', commit='d2048981696564ec75f661ed665977d3a6e09188')
    version('1.16.7', commit='fc560ed15ef7393a73d35e714716cc24dc835339')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-org-hs-eg-db', type=('build', 'run'))
    depends_on('r-kegggraph', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rgraphviz', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-keggrest', type=('build', 'run'))
