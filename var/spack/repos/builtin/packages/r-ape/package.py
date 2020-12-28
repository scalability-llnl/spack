# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RApe(RPackage):
    """Functions for reading, writing, plotting, and manipulating phylogenetic
    trees, analyses of comparative data in a phylogenetic framework, ancestral
    character analyses, analyses of diversification and macroevolution,
    computing distances from DNA sequences, reading and writing nucleotide
    sequences as well as importing from BioConductor, and several tools such
    as Mantel's test, generalized skyline plots, graphical exploration of
    phylogenetic data (alex, trex, kronoviz), estimation of absolute
    evolutionary rates and clock-like trees using mean path lengths and
    penalized likelihood, dating trees with non-contemporaneous sequences,
    translating DNA into AA sequences, and assessing sequence alignments.
    Phylogeny estimation can be done with the NJ, BIONJ, ME, MVR, SDM, and
    triangle methods, and several methods handling incomplete distance
    matrices (NJ*, BIONJ*, MVR*, and the corresponding triangle method). Some
    functions call external applications (PhyML, Clustal, T-Coffee, Muscle)
    whose results are returned into R."""

    homepage = "http://ape-package.ird.fr/"
    url      = "https://cloud.r-project.org/src/contrib/ape_4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ape"

    version('5.3', sha256='08b0df134c523feb00a86896d1aa2a43f0f0dab20a53bc6b5d6268d867988b23')
    version('5.2', sha256='27eb02856c130d59de6e06276be4981709923756319e465a7f2d4756d4f46415')
    version('5.1', sha256='b7d5dca66881638227a40aa59533904aa5efe0f4b867851b248e8f948a01a26e')
    version('5.0', sha256='c32ed22e350b3d7c7ef3de9334155ab1f3086922b5ec9a1643897cae7abda960')
    version('4.1', sha256='935af5ddadcba832d3f9cc032a80fc1a2e627a7ed54ef5f3773f87e06374a924')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
