# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcurl(RPackage):
    """A wrapper for 'libcurl' <http://curl.haxx.se/libcurl/> Provides
       functions to allow one to compose general HTTP requests and provides
       convenient functions to fetch URIs, get & post forms, etc. and process
       the results returned by the Web server. This provides a great deal of
       control over the HTTP/FTP/... connection and the form of the request
       while providing a higher-level interface than is available just using
       R socket connections. Additionally, the underlying implementation is
       robust and extensive, supporting FTP/FTPS/TFTP (uploads and downloads),
       SSL/HTTPS, telnet, dict, ldap, and also supports cookies, redirects,
       authentication, etc."""

    homepage = "https://cloud.r-project.org/package=RCurl"
    url      = "https://cloud.r-project.org/src/contrib/RCurl_1.95-4.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RCurl"

    version('1.98-1.2', sha256='5d74a0cdc3c5684b0348b959f67039e3c2a5da2bbb6176f6800a94124895a7a8')
    version('1.95-4.12', sha256='393779efafdf40823dac942a1e028905d65c34f3d41cfd21bcd225e411385ff4')
    version('1.95-4.8', sha256='e72243251bbbec341bc5864305bb8cc23d311d19c5d0d9310afec7eb35aa2bfb')

    depends_on('r@3.4.0:', when='@1.98:', type=('build', 'run'))
    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-bitops', type=('build', 'run'))
    depends_on('curl')
    depends_on('gmake', type='build')
