# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDose(RPackage):
    """Disease Ontology Semantic and Enrichment analysis.

       This package implements five methods proposed by Resnik, Schlicker,
       Jiang, Lin and Wang respectively for measuring semantic similarities
       among DO terms and gene products. Enrichment analyses including
       hypergeometric model and gene set enrichment analysis are also
       implemented for discovering disease associations of high-throughput
       biological data."""

    homepage = "https://bioconductor.org/packages/DOSE"
    git      = "https://git.bioconductor.org/packages/DOSE.git"

    version('3.10.2', commit='5ea51a2e2a04b4f3cc974cecb4537e14efd6a7e3')
    version('3.8.2', commit='4d3d1ca710aa7e4288a412c8d52b054b86a57639')
    version('3.6.1', commit='f2967f0482cea39222bfd15767d0f4a5994f241b')
    version('3.4.0', commit='dabb70de1a0f91d1767601e871f2f1c16d29a612')
    version('3.2.0', commit='71f563fc39d02dfdf65184c94e0890a63b96b86b')

    depends_on('r@3.3.1:', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-do-db', type=('build', 'run'))
    depends_on('r-fgsea', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gosemsim@2.0.0:', type=('build', 'run'))
    depends_on('r-igraph', when='@3.2.0:3.4.0', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-scales', when='@3.2.0:3.4.0', type=('build', 'run'))

    depends_on('r-rvcheck', when='@3.4.0', type=('build', 'run'))

    depends_on('r@3.4.0:', when='@3.6.1:', type=('build', 'run'))
