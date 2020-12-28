# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRspectra(RPackage):
    """R interface to the 'Spectra' library <https://spectralib.org/> for
    large-scale eigenvalue and SVD problems. It is typically used to compute a
    few eigenvalues/vectors of an n by n matrix, e.g., the k largest
    eigenvalues, which is usually more efficient than eigen() if k << n. This
    package provides the 'eigs()' function that does the similar job as in
    'Matlab', 'Octave', 'Python SciPy' and 'Julia'. It also provides the
    'svds()' function to calculate the largest k singular values and
    corresponding singular vectors of a real matrix. The matrix to be computed
    on can be dense, sparse, or in the form of an operator defined by the
    user."""

    homepage = "https://github.com/yixuan/RSpectra"
    url      = "https://cloud.r-project.org/src/contrib/RSpectra_0.15-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RSpectra"

    version('0.15-0', sha256='1ad5698201007044a0420cb10b7c48e94312a8a1d22b9d946d5de1c6743969a9')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-matrix@1.1-0:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.5:', type=('build', 'run'))
    depends_on('r-rcppeigen@0.3.3.3.0:', type=('build', 'run'))
