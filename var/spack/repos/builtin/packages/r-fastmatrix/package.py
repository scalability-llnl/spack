# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastmatrix(RPackage):
    """Fast Computation of some Matrices Useful in Statistics.

    Small set of functions to fast computation of some matrices and operations
    useful in statistics and econometrics. Currently, there are functions for
    efficient computation of duplication, commutation and symmetrizer matrices
    with minimal storage requirements. Some commonly used matrix decompositions
    (LU and LDL), basic matrix operations (for instance, Hadamard, Kronecker
    products and the Sherman-Morrison formula) and iterative solvers for linear
    systems are also available. In addition, the package includes a number of
    common statistical procedures such as the sweep operator, weighted mean and
    covariance matrix using an online algorithm, linear regression (using
    Cholesky, QR, SVD, sweep operator and conjugate gradients methods), ridge
    regression (with optimal selection of the ridge parameter considering the
    GCV procedure), functions to compute the multivariate skewness, kurtosis,
    Mahalanobis distance (checking the positive defineteness) and the
    Wilson-Hilferty transformation of chi squared variables. Furthermore, the
    package provides interfaces to C code callable by another C code from other
    R packages."""

    cran = "fastmatrix"

    license("GPL-3.0-only")

    version("0.5-772", sha256="72601bae9a59f467c5da9ccf08788f0233cdbb2420b6b2aa43a42a2632ff9c55")
    version("0.5", sha256="fb5f251a98425161e9dbbbb7edf95226725255b1474aad03ab046c7c6c6c3f12")
    version("0.4-1245", sha256="ee2e12b5dcda4585cca21f2c0ac144706f6fd26024586e91d622c6cd66d1d873")
    version("0.4-1", sha256="494a1aad38dcec28956eba8d095c964b20c5388dfb6dc2a23848ae37ea61cde5")
    version("0.3-8196", sha256="72fae07c627b995a091ccc3e14b2b2167474e3b1f14d723e87252538cf978fb6")
    version("0.3", sha256="d92e789454a129db5f6f5b23e0d2245f3d55ff34b167427af265b9a6331e7c21")

    depends_on("r@3.5.0:", type=("build", "run"))
