# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGosemsim(RPackage):
    """GO-terms Semantic Similarity Measures.

       The semantic comparisons of Gene Ontology (GO) annotations provide
       quantitative ways to compute similarities between genes and gene groups,
       and have became important basis for many bioinformatics analysis
       approaches. GOSemSim is an R package for semantic similarity computation
       among GO terms, sets of GO terms, gene products and gene clusters.
       GOSemSim implemented five methods proposed by Resnik, Schlicker, Jiang,
       Lin and Wang respectively."""

    homepage = "https://bioconductor.org/packages/GOSemSim"
    git      = "https://git.bioconductor.org/packages/GOSemSim.git"

    version('2.10.0', commit='5db1ecbf2f8d870430d6e587609327d05ba3ad7b')
    version('2.8.0', commit='c8c985b2a814cc2365c7f05b2509205e1b6b7f58')
    version('2.6.2', commit='2ffe78e89276e804306554965fc0799318ec56ed')
    version('2.4.1', commit='0656e845860d14e054670ffc246a1c53f699299c')
    version('2.2.0', commit='247434790e6c8cf99e5643f569390362b8c87c52')

    depends_on('r@3.3.2:', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))

    depends_on('r@3.4.0:', when='@2.8.0:', type=('build', 'run'))
