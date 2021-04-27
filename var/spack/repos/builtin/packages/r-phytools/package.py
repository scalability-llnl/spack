# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPhytools(RPackage):
    """Phylogenetic Tools for Comparative Biology (and Other Things)

    A wide range of functions for phylogenetic analysis. Functionality is
    concentrated in phylogenetic comparative biology, but also includes
    numerous methods for visualizing, manipulating, reading or writing, and
    even inferring phylogenetic trees and data. Included among the functions in
    phylogenetic comparative biology are various for ancestral state
    reconstruction, model-fitting, simulation of phylogenies and data, and
    multivariate analysis. There are a broad range of plotting methods for
    phylogenies and comparative data which include, but are not restricted to,
    methods for mapping trait evolution on trees, for projecting trees into
    phenotypic space or a geographic map, and for visualizing correlated
    speciation between trees. Finally, there are a number of functions for
    reading, writing, analyzing, inferring, simulating, and manipulating
    phylogenetic trees and comparative data not covered by other packages. For
    instance, there are functions for randomly or non-randomly attaching
    species or clades to a phylogeny, for estimating supertrees or consensus
    phylogenies from a set, for simulating trees and phylogenetic data under a
    range of models, and for a wide variety of other manipulations and analyses
    that phylogenetic biologists might find useful in their research."""

    homepage = "http://github.com/liamrevell/phytools"
    url      = "https://cloud.r-project.org/src/contrib/phytools_0.6-60.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/phytools/"

    version('0.7-70', sha256='e3432c3b006e5cc6f1292bebd81ebc20044edf1f56c3d27a3497f738eb99f0d3')
    version('0.6-99', sha256='2ef532cba77c5f73803bd34582bef05709705311a0b50e42316e69944567390f')
    version('0.6-60', sha256='55cad759510d247ebbf03a53a46caddadd3bf87584ccf7fcd6dd06d44516b377')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@0.7-70:', type=('build', 'run'))
    depends_on('r-ape@4.0:', type=('build', 'run'))
    depends_on('r-maps', type=('build', 'run'))
    depends_on('r-clustergeneration', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-combinat', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-gtools', when='@0.6-99:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-phangorn@2.3.1:', type=('build', 'run'))
    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-animation', when='@:0.6-99', type=('build', 'run'))
