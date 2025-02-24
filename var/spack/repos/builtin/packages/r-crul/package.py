# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCrul(RPackage):
    """HTTP Client.

    A simple HTTP client, with tools for making HTTP requests, and mocking HTTP
    requests. The package is built on R6, and takes inspiration from Ruby's
    'faraday' gem (<https://rubygems.org/gems/faraday>). The package name is a
    play on curl, the widely used command line tool for HTTP, and this package
    is built on top of the R package 'curl', an interface to 'libcurl'
    (<https://curl.haxx.se/libcurl>)."""

    cran = "crul"

    license("MIT")

    version("1.5.0", sha256="db733778d2815f9d974b00e8df7c821cd638e069e08d73adfa606add201ebd9d")
    version("1.3", sha256="8058617d8b3724acb5b89d0e6e63f381df5c56565128b250a65eceb2b8081e2d")
    version("1.2.0", sha256="be1a149b21cf219ef55adfb56a6a5eb9892a9acf0d5f5421a22e52f2a7066f8c")
    version("1.0.0", sha256="2ade500f6cf89b2d0ca8496b8d4df9937d6f802a35c9ad10d9fab8632cdb1027")
    version("0.8.4", sha256="dbd950ad3b68402e5a5955615b1abcb5c9bdc846c93aa25f96a7a58913d04c8b")
    version("0.7.4", sha256="c963dd666ae3fc89b661ce19fce2fa19a16fc3825e1502105cae98ceb92c6014")

    depends_on("r-curl@3.3:", type=("build", "run"))
    depends_on("r-r6@2.2.0:", type=("build", "run"))
    depends_on("r-urltools@1.6.0:", type=("build", "run"))
    depends_on("r-httpcode@0.2.0:", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"), when="@0.8.4:")
    depends_on("r-mime", type=("build", "run"))
