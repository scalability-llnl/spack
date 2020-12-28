# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bitmap(AutotoolsPackage, XorgPackage):
    """bitmap, bmtoa, atobm - X bitmap (XBM) editor and converter utilities."""

    homepage = "http://cgit.freedesktop.org/xorg/app/bitmap"
    xorg_mirror_path = "app/bitmap-1.0.8.tar.gz"

    version('1.0.8', sha256='1a2fbd10a2ca5cd93f7b77bbb0555b86d8b35e0fc18d036b1607c761755006fc')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')

    depends_on('xbitmaps', type='build')
    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
