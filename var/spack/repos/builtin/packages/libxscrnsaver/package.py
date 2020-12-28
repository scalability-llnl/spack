# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxscrnsaver(AutotoolsPackage, XorgPackage):
    """XScreenSaver - X11 Screen Saver extension client library"""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXScrnSaver"
    xorg_mirror_path = "lib/libXScrnSaver-1.2.2.tar.gz"

    version('1.2.2', sha256='e12ba814d44f7b58534c0d8521e2d4574f7bf2787da405de4341c3b9f4cc8d96')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('scrnsaverproto@1.2:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
