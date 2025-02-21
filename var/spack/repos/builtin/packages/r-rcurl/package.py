# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcurl(RPackage):
    """General Network (HTTP/FTP/...) Client Interface for R.

    A wrapper for 'libcurl' <http://curl.haxx.se/libcurl/> Provides functions
    to allow one to compose general HTTP requests and provides convenient
    functions to fetch URIs, get & post forms, etc. and process the results
    returned by the Web server. This provides a great deal of control over the
    HTTP/FTP/... connection and the form of the request while providing a
    higher-level interface than is available just using R socket connections.
    Additionally, the underlying implementation is robust and extensive,
    supporting FTP/FTPS/TFTP (uploads and downloads), SSL/HTTPS, telnet, dict,
    ldap, and also supports cookies, redirects, authentication, etc."""

    cran = "RCurl"

    version("1.98-1.16", sha256="1a8dc40e10593617348071c6265cc7fac22e26271564206b308a3badfc6c0da7")
    version("1.98-1.12", sha256="1a83fef04e9573b402171a6e4a4b27857a3d045eec8970f8f7233850bba626b2")
    version("1.98-1.9", sha256="f28d4871675ec3d2b45fb5d36f7647f546f81121510954c3ad24fdec1643cec5")
    version("1.98-1.6", sha256="6cb56864ac043195b658bbdb345518d561507d84ccd60362866e970c2f71d1a2")
    version("1.98-1.5", sha256="73187c9a039188ffdc255fb7fa53811a6abfb31e6375a51eae8c763b37dd698d")
    version("1.98-1.2", sha256="5d74a0cdc3c5684b0348b959f67039e3c2a5da2bbb6176f6800a94124895a7a8")
    version("1.95-4.12", sha256="393779efafdf40823dac942a1e028905d65c34f3d41cfd21bcd225e411385ff4")
    version("1.95-4.8", sha256="e72243251bbbec341bc5864305bb8cc23d311d19c5d0d9310afec7eb35aa2bfb")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.98:")
    depends_on("r-bitops", type=("build", "run"))
    depends_on("curl")
    depends_on("gmake", type="build")
