# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSctransform(RPackage):
    """Variance Stabilizing Transformations for Single Cell UMI Data

    A normalization method for single-cell UMI count data using a variance
    stabilizing transformation. The transformation is based on a negative
    binomial regression model with regularized parameters. As part of the same
    regression framework, this package also provides functions for batch
    correction, and data correction. See Hafemeister and Satija 2019
    <doi:10.1101/576827> for more details."""

    homepage = "https://github.com/ChristophH/sctransform"
    url      = "https://cloud.r-project.org/src/contrib/sctransform_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sctransform"

    version('0.3.2', sha256='5dbb0a045e514c19f51bbe11c2dba0b72dca1942d6eb044c36b0538b443475dc')
    version('0.2.0', sha256='d7f4c7958693823454f1426b23b0e1e9c207ad61a7a228602a1885a1318eb3e4')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@0.3.2:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-future-apply', type=('build', 'run'))
    depends_on('r-future', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-matrixstats', when='@0.3.2:', type=('build', 'run'))
    depends_on('r-rcpparmadillo', when='@0.3.2:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rcppeigen', when='@:0.2.0', type=('build', 'run'))
