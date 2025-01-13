# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpphnsw(RPackage):
    """'Rcpp' Bindings for 'hnswlib', a Library for Approximate
    NearestNeighbors.

    'Hnswlib' is a C++ library for Approximate Nearest Neighbors. This ;
    package provides a minimal R interface by relying on the 'Rcpp' package.
    See ; <https://github.com/nmslib/hnswlib> for more on 'hnswlib'. 'hnswlib'
    is ; released under Version 2.0 of the Apache License."""

    cran = "RcppHNSW"

    version("0.6.0", sha256="a5a6ed00a84143aa62aa67df66fcccae657d5db0a1f9bb4b955a8e94c2ff580f")
    version("0.4.1", sha256="4f0082154f77dcb7756d41cdbfe0f58316431b9027081321a27942f319097c74")
    version("0.3.0", sha256="a0eb4eea65e28ba31e8306a1856f7e617a192bd448b148f88abe99181cbde007")
    version("0.1.0", sha256="75a54c30953845dec685764c7b3b4cd7315197c91aef4ab3b4eb0a6293010a95")

    depends_on("r-rcpp@0.11.3:", type=("build", "run"))
