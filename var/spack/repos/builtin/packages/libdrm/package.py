# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Libdrm(AutotoolsPackage):
    """A userspace library for accessing the DRM, direct rendering manager,
    on Linux, BSD and other systems supporting the ioctl interface."""

    homepage = "http://dri.freedesktop.org/libdrm/"
    url      = "https://dri.freedesktop.org/libdrm/libdrm-2.4.59.tar.gz"

    version('2.4.100', sha256='6a5337c054c0c47bc16607a21efa2b622e08030be4101ef4a241c5eb05b6619b')
    version('2.4.81',  sha256='64036c5e0668fdc2b820dcc0ebab712f44fd2c2147d23dc5a6e003b19f0d3e9f')
    version('2.4.75',  sha256='a411bff814b4336c8908dcbd045cd89fdc7afedc75b795d897d462e467cbb01d')
    version('2.4.70',  sha256='73615b9c1c4852e5ce045efa19c866e8df98e396b2443bf859eea05574ecb64f')
    version('2.4.59',  sha256='ed9d03a92c2d80e6310cc350db3430620f1659ae084a07c6824cee7bc81ae8fa')
    version('2.4.33',  sha256='bd2a8fecf28616f2157ca33ede691c139cc294ed2d0c4244b62ca7d22e98e5a4')

    depends_on('pkgconfig', type='build')
    depends_on('libpciaccess@0.10:', when=(sys.platform != 'darwin'))
    depends_on('libpthread-stubs')

    def configure_args(self):
        args = []
        args.append('--enable-static')
        args.append('LIBS=-lrt')  # This fixes a bug with `make check`
        if self.spec.satisfies('%gcc@10.0.0:'):
            args.append('CFLAGS=-fcommon')
        return args
