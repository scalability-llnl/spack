# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxt(AutotoolsPackage, XorgPackage):
    """libXt - X Toolkit Intrinsics library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXt"
    xorg_mirror_path = "lib/libXt-1.1.5.tar.gz"

    version('1.1.5', sha256='b59bee38a9935565fa49dc1bfe84cb30173e2e07e1dcdf801430d4b54eb0caa3')

    depends_on('libsm')
    depends_on('libice')
    depends_on('libx11')

    depends_on('xproto', type='build')
    depends_on('kbproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    @property
    def libs(self):
        return find_libraries(
            'libXt', root=self.prefix, shared=True, recursive=True
        )
