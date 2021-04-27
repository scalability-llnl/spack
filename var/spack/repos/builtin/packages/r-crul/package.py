# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCrul(RPackage):
    """HTTP Client

    A simple HTTP client, with tools for making HTTP requests, and mocking HTTP
    requests. The package is built on R6, and takes inspiration from Ruby's
    'faraday' gem (<https://rubygems.org/gems/faraday>). The package name is a
    play on curl, the widely used command line tool for HTTP, and this package
    is built on top of the R package 'curl', an interface to 'libcurl'
    (<https://curl.haxx.se/libcurl>)."""

    homepage = "https://cloud.r-project.org/package=crul"
    url      = "https://cloud.r-project.org/src/contrib/crul_0.7.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/crul"

    version('1.0.0', sha256='2ade500f6cf89b2d0ca8496b8d4df9937d6f802a35c9ad10d9fab8632cdb1027')
    version('0.8.4', sha256='dbd950ad3b68402e5a5955615b1abcb5c9bdc846c93aa25f96a7a58913d04c8b')
    version('0.7.4', sha256='c963dd666ae3fc89b661ce19fce2fa19a16fc3825e1502105cae98ceb92c6014')

    depends_on('r-curl@3.3:', type=('build', 'run'))
    depends_on('r-r6@2.2.0:', type=('build', 'run'))
    depends_on('r-urltools@1.6.0:', type=('build', 'run'))
    depends_on('r-httpcode@0.2.0:', type=('build', 'run'))
    depends_on('r-jsonlite', when='@0.8.4:', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
