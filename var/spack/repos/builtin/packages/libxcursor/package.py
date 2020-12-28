# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcursor(AutotoolsPackage, XorgPackage):
    """libXcursor - X Window System Cursor management library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXcursor"
    xorg_mirror_path = "lib/libXcursor-1.1.14.tar.gz"

    version('1.1.14', sha256='be0954faf274969ffa6d95b9606b9c0cfee28c13b6fc014f15606a0c8b05c17b')

    depends_on('libxrender@0.8.2:')
    depends_on('libxfixes')
    depends_on('libx11')

    depends_on('fixesproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
