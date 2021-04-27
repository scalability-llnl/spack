# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRcpphnsw(RPackage):
    """'Rcpp' Bindings for 'hnswlib', a Library for Approximate
       NearestNeighbors

    'Hnswlib' is a C++ library for Approximate Nearest Neighbors. This ;
    package provides a minimal R interface by relying on the 'Rcpp' package.
    See ; <https://github.com/nmslib/hnswlib> for more on 'hnswlib'. 'hnswlib'
    is ; released under Version 2.0 of the Apache License."""

    homepage = "https://cloud.r-project.org/package=RcppHNSW"
    url      = "https://cloud.r-project.org/src/contrib/RcppHNSW_0.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppHNSW"

    version('0.3.0', sha256='a0eb4eea65e28ba31e8306a1856f7e617a192bd448b148f88abe99181cbde007')
    version('0.1.0', sha256='75a54c30953845dec685764c7b3b4cd7315197c91aef4ab3b4eb0a6293010a95')

    depends_on('r-rcpp@0.11.3:', type=('build', 'run'))
