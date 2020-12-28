# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxxf86misc(AutotoolsPackage, XorgPackage):
    """libXxf86misc - Extension library for the XFree86-Misc X extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86misc"
    xorg_mirror_path = "lib/libXxf86misc-1.0.3.tar.gz"

    version('1.0.3', sha256='358f692f793af00f6ef4c7a8566c1bcaeeea37e417337db3f519522cc1df3946')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86miscproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
