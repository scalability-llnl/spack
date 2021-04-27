# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RFastmatrix(RPackage):
    """Fast Computation of some Matrices Useful in Statistics

    Small set of functions to fast computation of some matrices and operations
    useful in statistics."""

    homepage = "https://faosorios.github.io/fastmatrix/"
    url      = "https://cloud.r-project.org/src/contrib/fastmatrix_0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fastmatrix"

    version('0.3', sha256='d92e789454a129db5f6f5b23e0d2245f3d55ff34b167427af265b9a6331e7c21')

    depends_on('r@3.5.0:', type=('build', 'run'))
