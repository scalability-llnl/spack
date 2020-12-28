# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdephylo(RPackage):
    """adephylo: Exploratory Analyses for the Phylogenetic Comparative Method.

    Multivariate tools to analyze comparative data, i.e. a phylogeny and
    some traits measured for each taxa."""

    homepage = "https://cloud.r-project.org/package=adephylo"
    url      = "https://cloud.r-project.org/src/contrib/adephylo_1.1-11.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/adephylo"

    version('1.1-11', sha256='154bf2645eac4493b85877933b9445442524ca4891aefe4e80c294c398cff61a')

    depends_on('r-ade4@1.7-10:', type=('build', 'run'))
    depends_on('r-phylobase', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-adegenet', type=('build', 'run'))
