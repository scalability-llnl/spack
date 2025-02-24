# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppeigen(RPackage):
    """'Rcpp' Integration for the 'Eigen' Templated Linear Algebra Library.

    R and 'Eigen' integration using 'Rcpp'. 'Eigen' is a C++ template library
    for linear algebra: matrices, vectors, numerical solvers and related
    algorithms. It supports dense and sparse matrices on integer, floating
    point and complex numbers, decompositions of such matrices, and solutions
    of linear systems. Its performance on many algorithms is comparable with
    some of the best implementations based on 'Lapack' and level-3 'BLAS'. The
    'RcppEigen' package includes the header files from the 'Eigen' C++ template
    library (currently version 3.2.8). Thus users do not need to install
    'Eigen' itself in order to use 'RcppEigen'. Since version 3.1.1, 'Eigen' is
    licensed under the Mozilla Public License (version 2); earlier version were
    licensed under the GNU LGPL version 3 or later.  'RcppEigen' (the 'Rcpp'
    bindings/bridge to 'Eigen') is licensed under the GNU GPL version 2 or
    later, as is the rest of 'Rcpp'."""

    cran = "RcppEigen"

    license("MPL-2.0")

    version("0.3.4.0.1", sha256="25ed48f148b50aaadd92752d73e3eefe00ab4ecd4ae5662ae91a9ff3f72a4e26")
    version("0.3.3.9.3", sha256="5873a47fd6587d916f86119ab140c6736abf80ac45d06ff1c9d198708e7d1c76")
    version("0.3.3.9.2", sha256="2547e794d5a6fb8d9fbadf19e64afa0bcf413cc69ecf3f428995fa5a0fced493")
    version("0.3.3.9.1", sha256="8a0486249b778a4275a1168fc89fc7fc49c2bb031cb14b50a50089acae7fe962")
    version("0.3.3.5.0", sha256="e5c6af17770c5f57b7cf2fba04ad1a519901b446e8138bfff221952458207f05")
    version("0.3.3.4.0", sha256="11020c567b299b1eac95e8a4d57abf0315931286907823dc7b66c44d0dd6dad4")
    version("0.3.3.3.1", sha256="14fdd2cb764d0a822e11b8f09dcf1c3c8580d416f053404732064d8f2b176f24")
    version("0.3.2.9.0", sha256="25affba9065e3c12d67b1934d1ce97a928a4011a7738f7b90f0e9830409ec93b")
    version("0.3.2.8.1", sha256="ceccb8785531c5c23f9232b594e5372c214a114a08ec759115e946badd08d681")

    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.3.3.9.3:")

    depends_on("r-matrix@1.1-0:", type=("build", "run"), when="@:0.3.3.9.3")
