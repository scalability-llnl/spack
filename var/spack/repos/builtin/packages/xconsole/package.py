# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xconsole(AutotoolsPackage, XorgPackage):
    """xconsole displays in a X11 window the messages which are usually sent
    to /dev/console."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xconsole"
    xorg_mirror_path = "app/xconsole-1.0.6.tar.gz"

    version('1.0.6', sha256='28151453a0a687462516de133bac0287b488a2ff56da78331fee34bc1bf3e7d5')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.0:')
    depends_on('libx11')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
