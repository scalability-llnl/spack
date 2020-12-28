# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhangorn(RPackage):
    """Package contains methods for estimation of phylogenetic trees and
       networks using Maximum Likelihood, Maximum Parsimony, distance methods
       and Hadamard conjugation. Allows to compare trees, models selection and
       offers visualizations for trees and split networks."""

    homepage = "https://cloud.r-project.org/package=phangorn"
    url      = "https://cloud.r-project.org/src/contrib/phangorn_2.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/phangorn"

    version('2.5.5', sha256='c58dc1ace26cb4358619a15da3ea4765dbdde1557acccc5103c85589a7571346')
    version('2.5.3', sha256='a306585a0aabe7360a2adaf9116ae2993fb5ceff641b198f2e01e4329d3768af')
    version('2.3.1', sha256='518c31f5b2c5f0a655d02a3c71b00c30caea2794dfc31f9d63f3d505bd7863eb')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-ape@5.0:', type=('build', 'run'))
    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-igraph@1.0:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-fastmatch', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
