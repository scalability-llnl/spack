# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQs(RPackage):
    """Quick Serialization of R Objects

    Provides functions for quickly writing and reading any R object
    to and from disk."""

    homepage = "https://cloud.r-project.org/web/packages/qs/index.html"
    url      = "https://cloud.r-project.org/src/contrib/qs_0.23.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/qs"

    maintainers = ['dorton21']

    version('0.23.6', sha256='c6e958e9741ee981bf2388c91b8f181718ffb0f32283cd7ebcd2d054817280e4')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rapiserialize', type=('build', 'run'))
    depends_on('r-stringfish@0.14.1:', type=('build', 'run'))
