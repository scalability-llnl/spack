# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBigalgebra(RPackage):
    """'BLAS' and 'LAPACK' Routines for Native R Matrices and 'big.matrix'
    Objects.

    Provides arithmetic functions for R matrix and 'big.matrix' objects as well
    as functions for QR factorization, Cholesky factorization, General
    eigenvalue, and Singular value decomposition (SVD). A method matrix
    multiplication and an arithmetic method -for matrix addition, matrix
    difference- allows for mixed type operation -a matrix class object and a
    big.matrix class object- and pure type operation for two big.matrix class
    objects."""

    cran = "bigalgebra"

    license("LGPL-3.0-only OR Apache-2.0")

    version("1.1.1", sha256="fc6a48b940cca86caf8372648a1b1e4066f2f6d618a77303a1c8766c5b7bbf1f")
    version("1.1.0", sha256="e51530287a64826a3dfb55f41594bc8123b7b4c9b2074f6c8de218fa8b525734")
    version("1.0.1", sha256="ff7e261d0aa0e0f498e926d923ac62fc5cb783fa1f74bb2ff76a09167388a9d2")
    version("1.0.0", sha256="f186b603bd660be0cc5b7a52c943e23e92fef264f0bc96a8858e38df6cfc4085")
    version("0.8.4.2", sha256="29962468cbfa6416f8628563d5ed8c9f76089190311ff1c618f099ee8d9eea75")

    depends_on("r-bigmemory@4.0.0:", type=("build", "run"))
    depends_on("r-bh", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"), when="@1.0.0:")
