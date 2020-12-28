# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHttpuv(RPackage):
    """Provides low-level socket and protocol support for handling HTTP and
    WebSocket requests directly from within R. It is primarily intended as a
    building block for other packages, rather than making it particularly easy
    to create complete web applications using httpuv alone. httpuv is built on
    top of the libuv and http-parser C libraries, both of which were developed
    by Joyent, Inc. (See LICENSE file for libuv and http-parser license
    information.)"""

    homepage = "https://github.com/rstudio/httpuv"
    url      = "https://cloud.r-project.org/src/contrib/httpuv_1.3.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/httpuv"

    version('1.5.1', sha256='b5bb6b3b2f1a6d792568a70f3f357d6b3a35a5e26dd0c668c61a31f2ae8f5710')
    version('1.3.5', sha256='4336b993afccca2a194aca577b1975b89a35ac863423b18a11cdbb3f8470e4e9')
    version('1.3.3', sha256='bb37452ddc4d9381bee84cdf524582859af6a988e291debb71c8a2e120d02b2a')

    depends_on('r@2.15.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-r6', when='@1.5.0:', type=('build', 'run'))
    depends_on('r-promises', when='@1.5.0:', type=('build', 'run'))
    depends_on('r-later@0.8.0:', when='@1.5.0:', type=('build', 'run'))
    depends_on('gmake', type='build')
