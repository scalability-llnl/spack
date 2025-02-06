# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRspectra(RPackage):
    """Solvers for Large-Scale Eigenvalue and SVD Problems.

    R interface to the 'Spectra' library <https://spectralib.org/> for
    large-scale eigenvalue and SVD problems. It is typically used to compute a
    few eigenvalues/vectors of an n by n matrix, e.g., the k largest
    eigenvalues, which is usually more efficient than eigen() if k << n. This
    package provides the 'eigs()' function that does the similar job as in
    'Matlab', 'Octave', 'Python SciPy' and 'Julia'. It also provides the
    'svds()' function to calculate the largest k singular values and
    corresponding singular vectors of a real matrix. The matrix to be computed
    on can be dense, sparse, or in the form of an operator defined by the
    user."""

    cran = "RSpectra"

    version("0.16-2", sha256="a2f149d79519fee79dabe1b174dfb847a916045315d5927a93cc6b005522aa7e")
    version("0.16-1", sha256="cba5d3403d6a7d0e27abf6279fbfea6e0d0fe36b28c688bbadb8eafb3841329a")
    version("0.16-0", sha256="aaf1cfc9ffe3a4c6684247899924e1c18306971dfef4bae1dc596a2fb42a64a9")
    version("0.15-0", sha256="1ad5698201007044a0420cb10b7c48e94312a8a1d22b9d946d5de1c6743969a9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-matrix@1.1-0:", type=("build", "run"))
    depends_on("r-rcpp@0.11.5:", type=("build", "run"))
    depends_on("r-rcppeigen@0.3.3.3.0:", type=("build", "run"))
