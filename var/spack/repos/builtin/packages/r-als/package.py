# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAls(RPackage):
    """Alternating least squares is often used to resolve components
    contributing to data with a bilinear structure; the basic
    technique may be extended to alternating constrained least squares.
    Commonly applied constraints include unimodality, non-negativity,
    and normalization of components. Several data matrices may be
    decomposed simultaneously by assuming that one of the two matrices
    in the bilinear decomposition is shared between datasets."""

    homepage = "https://cloud.r-project.org/package=ALS"
    url      = "https://cloud.r-project.org/src/contrib/ALS_0.0.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ALS"

    version('0.0.6', sha256='ca90d27115ae9e476967f521bf6935723e410a3bf92477e7570e14bfd3b099eb')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-iso', type=('build', 'run'))
    depends_on('r-nnls@1.1:', type=('build', 'run'))
