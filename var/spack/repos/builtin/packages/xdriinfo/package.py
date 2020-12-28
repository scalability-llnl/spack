# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdriinfo(AutotoolsPackage, XorgPackage):
    """xdriinfo - query configuration information of X11 DRI drivers."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xdriinfo"
    xorg_mirror_path = "app/xdriinfo-1.0.5.tar.gz"

    version('1.0.5', sha256='e4e6abaa4591c540ab63133927a6cebf0a5f4d27dcd978878ab4a422d62a838e')

    depends_on('libx11')
    depends_on('expat')
    depends_on('libxshmfence')
    depends_on('libxext')
    depends_on('libxdamage')
    depends_on('libxfixes')
    depends_on('pcre')

    depends_on('glproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
