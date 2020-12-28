# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Netdata(AutotoolsPackage):
    """Real-time performance monitoring, done right!"""

    homepage = "https://www.netdata.cloud/"
    url      = "https://github.com/netdata/netdata/archive/v1.22.1.tar.gz"

    version('1.22.1', sha256='6efd785eab82f98892b4b4017cadfa4ce1688985915499bc75f2f888765a3446')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('libuv')
    depends_on('libuuid')
