# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxdamage(AutotoolsPackage, XorgPackage):
    """This package contains the library for the X Damage extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXdamage"
    xorg_mirror_path = "lib/libXdamage-1.1.4.tar.gz"

    version('1.1.4', sha256='4bb3e9d917f5f593df2277d452926ee6ad96de7b7cd1017cbcf4579fe5d3442b')

    depends_on('libxfixes')
    depends_on('libx11')

    depends_on('damageproto@1.1:', type='build')
    depends_on('fixesproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
