# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSparsematrixstats(RPackage):
    """Summary Statistics for Rows and Columns of Sparse Matrices.

    High performance functions for row and column operations on sparse
    matrices.  For example: col / rowMeans2, col / rowMedians, col / rowVars
    etc. Currently, the optimizations are limited to data in the column sparse
    format.  This package is inspired by the matrixStats package by Henrik
    Bengtsson."""

    bioc = "sparseMatrixStats"

    # The repository is at
    # https://code.bioconductor.org/browse/sparseMatrixStats/, to find the
    # commit hash check the branch corresponding to a BioConductor release and
    # the latest commit (or one of the latest ones) should be the one bumping
    # the r-sparsematrixstats version.
    version("1.18.0", commit="172c63ee6c8fa200d2fda5546750ab5ac8ddd858")
    version("1.16.0", commit="2ad650c393497263c20d67d45d1a56ee6fa3b402")
    version("1.14.0", commit="2923a3bb4e59cf0e05f0e21a8e8df66e670c4abc")
    version("1.12.0", commit="054bf939cd7220deaf8e768ff7029d0d38483c91")
    version("1.10.0", commit="75d85ba2c9c4c36887fef1a007883167aa85bd94")
    version("1.8.0", commit="4f1e2213e5b0d6b3d817c2c9129b7566288916f6")
    version("1.6.0", commit="78627a842790af42b6634893087b2bb1f4ac0392")
    version("1.2.1", commit="9726f3d5e0f03b50c332d85d5e4c339c18b0494c")

    depends_on("cxx", type="build")  # generated

    depends_on("r-matrixgenerics", type=("build", "run"))
    depends_on("r-matrixgenerics@1.5.3:", type=("build", "run"), when="@1.6.0:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-matrixstats@0.60.0:0.63.0", type=("build", "run"), when="@1.6.0:1.12")
    # r-sparsematrixstats 1.12- is incompatible with r-matrixstats v1:
    # https://github.com/HenrikBengtsson/matrixStats/issues/227
    depends_on("r-matrixstats@1:", type=("build", "run"), when="@1.13.0:")
