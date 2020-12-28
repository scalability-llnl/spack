# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCurl(RPackage):
    """The curl() and curl_download() functions provide highly configurable
    drop-in replacements for base url() and download.file() with better
    performance, support for encryption (https, ftps), gzip compression,
    authentication, and other libcurl goodies. The core of the package
    implements a framework for performing fully customized requests where data
    can be processed either in memory, on disk, or streaming via the callback
    or connection interfaces. Some knowledge of libcurl is recommended; for a
    more-user-friendly web client see the 'httr' package which builds on this
    package with http specific tools and logic."""

    homepage = "https://github.com/jeroenooms/curl"
    url      = "https://cloud.r-project.org/src/contrib/curl_2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/curl"

    version('4.3', sha256='7406d485bb50a6190e3ed201e3489063fd249b8b3b1b4f049167ac405a352edb')
    version('4.0', sha256='09a99c9c86666449188fbb211cb1e9fbdb5108ab56f0d09322cd0ae50e926171')
    version('3.3', sha256='0cb0b9a9280edc42ebed94708541ec86b4f48779e722171e45227eab8a88a5bd')
    version('3.0', sha256='7bf8e3ae7cc77802ae300277e85d925d4c0611a9b7dad5c5601e0d2cbe14a506')
    version('2.3', sha256='f901dad6bb70a6875a85da75bcbb42afffdcdf4ef221909733826bcb012d7c3d')
    version('1.0', sha256='f8927228754fdfb21dbf08b9e67c5f97e06764c4adf327a4126eed84b1508f3d')
    version('0.9.7', sha256='46e150998723fd1937da598f47f49fe47e40c1f57ec594436c6ef1e0145b44dc')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('curl', when='@4.3:')
    depends_on('curl@:7.63', when='@:4.0')
