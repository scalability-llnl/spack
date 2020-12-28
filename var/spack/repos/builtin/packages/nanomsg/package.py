# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nanomsg(CMakePackage):
    """The nanomsg library is a simple high-performance
       implementation of several 'scalability protocols'"""

    homepage = "https://nanomsg.org/"
    url = "https://github.com/nanomsg/nanomsg/archive/1.0.0.tar.gz"

    version('1.1.5', sha256='218b31ae1534ab897cb5c419973603de9ca1a5f54df2e724ab4a188eb416df5a')
    version('1.0.0', sha256='24afdeb71b2e362e8a003a7ecc906e1b84fd9f56ce15ec567481d1bb33132cc7')
