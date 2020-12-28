# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRda(RPackage):
    """Shrunken Centroids Regularized Discriminant Analysis for the
    classification purpose in high dimensional data."""

    homepage = "https://cloud.r-project.org/package=rda"
    url      = "https://cloud.r-project.org/src/contrib/rda_1.0.2-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rda"

    version('1.0.2-2.1', sha256='6918b62f51252b57f2c05b99debef6136b370f594dc3ae6466268e4c35578ef8')
    version('1.0.2-2', sha256='52ee41249b860af81dc692eee38cd4f8f26d3fbe34cb274f4e118de0013b58bc')
    version('1.0.2-1', sha256='e5b96610ec9e82f12efe5dbb9a3ec9ecba9aaddfad1d6ab3f8c37d15fc2b42b7')

    depends_on('r@2.10:', type=('build', 'run'))
