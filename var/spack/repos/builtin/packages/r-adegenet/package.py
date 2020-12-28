# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdegenet(RPackage):
    """Toolset for the exploration of genetic and genomic data. Adegenet
    provides formal (S4) classes for storing and handling various genetic
    data, including genetic markers with varying ploidy and hierarchical
    population structure ('genind' class), alleles counts by populations
    ('genpop'), and genome-wide SNP data ('genlight'). It also implements
    original multivariate methods (DAPC, sPCA), graphics, statistical tests,
    simulation tools, distance and similarity measures, and several spatial
    methods. A range of both empirical and simulated datasets is also provided
    to illustrate various methods."""

    homepage = "https://github.com/thibautjombart/adegenet/wiki"
    url      = "https://cloud.r-project.org/src/contrib/adegenet_2.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/adegenet"

    version('2.1.1', sha256='3043fe5d731a38ff0e266f090dcda448640c3d0fd61934c76da32d082e5dce7a')
    version('2.1.0', sha256='7ee44061002b41164bbc09256307ab02e536f4f2ac03f36c7dc8f85f6af4639a')
    version('2.0.1', sha256='7eddf46e64f680d54d034b68c50900d9bd5bc2e08309d062e230121b7460bb10')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-seqinr', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-dplyr@0.4.1:', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'))
