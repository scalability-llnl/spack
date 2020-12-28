# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpphnsw(RPackage):
    """RcppHNSW: 'Rcpp' Bindings for 'hnswlib', a Library for Approximate
       NearestNeighbors"""

    homepage = "https://cloud.r-project.org/package=RcppHNSW"
    url      = "https://cloud.r-project.org/src/contrib/RcppHNSW_0.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppHNSW"

    version('0.1.0', sha256='75a54c30953845dec685764c7b3b4cd7315197c91aef4ab3b4eb0a6293010a95')

    depends_on('r-rcpp@0.11.3:', type=('build', 'run'))
