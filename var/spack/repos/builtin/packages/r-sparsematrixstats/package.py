# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSparsematrixstats(RPackage):
    """Summary Statistics for Rows and Columns of Sparse Matrices

    High performance functions for row and column operations on sparse
    matrices.  For example: col / rowMeans2, col / rowMedians, col / rowVars
    etc. Currently, the optimizations are limited to data in the column sparse
    format.  This package is inspired by the matrixStats package by Henrik
    Bengtsson."""

    homepage = "https://bioconductor.org/packages/sparseMatrixStats/"
    git      = "https://git.bioconductor.org/packages/sparseMatrixStats"

    version('1.2.1', commit='9726f3d5e0f03b50c332d85d5e4c339c18b0494c')

    depends_on('r-matrixgenerics', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
