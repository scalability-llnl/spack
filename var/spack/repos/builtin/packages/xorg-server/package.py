# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XorgServer(AutotoolsPackage, XorgPackage):
    """X.Org Server is the free and open source implementation of the display
    server for the X Window System stewarded by the X.Org Foundation."""

    homepage = "http://cgit.freedesktop.org/xorg/xserver"
    xorg_mirror_path = "xserver/xorg-server-1.18.99.901.tar.gz"

    version('1.18.99.901', sha256='c8425163b588de2ee7e5c8e65b0749f2710f55a7e02a8d1dc83b3630868ceb21')

    depends_on('pixman@0.27.2:')
    depends_on('font-util')
    depends_on('libxshmfence@1.1:')
    depends_on('libdrm@2.3.0:')
    depends_on('libx11')

    depends_on('dri2proto@2.8:', type='build')
    depends_on('dri3proto@1.0:', type='build')
    depends_on('glproto@1.4.17:', type='build')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('fixesproto@5.0:')
    depends_on('damageproto@1.1:')
    depends_on('xcmiscproto@1.2.0:')
    depends_on('xtrans@1.3.5:')
    depends_on('bigreqsproto@1.1.0:')
    depends_on('xproto@7.0.28:')
    depends_on('randrproto@1.5.0:')
    depends_on('renderproto@0.11:')
    depends_on('xextproto@7.2.99.901:')
    depends_on('inputproto@2.3:')
    depends_on('kbproto@1.0.3:')
    depends_on('fontsproto@2.1.3:')
    depends_on('pixman@0.27.2:')
    depends_on('videoproto')
    depends_on('compositeproto@0.4:')
    depends_on('recordproto@1.13.99.1:')
    depends_on('scrnsaverproto@1.1:')
    depends_on('resourceproto@1.2.0:')
    depends_on('xf86driproto@2.1.0:')
    depends_on('glproto@1.4.17:')
    depends_on('presentproto@1.0:')
    depends_on('xineramaproto')
    depends_on('libxkbfile')
    depends_on('libxfont2')
    depends_on('libxext')
    depends_on('libxdamage')
    depends_on('libxfixes')
    depends_on('libepoxy')
