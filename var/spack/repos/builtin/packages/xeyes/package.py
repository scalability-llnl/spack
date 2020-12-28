# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xeyes(AutotoolsPackage, XorgPackage):
    """xeyes - a follow the mouse X demo, using the X SHAPE extension"""

    homepage = "http://cgit.freedesktop.org/xorg/app/xeyes"
    xorg_mirror_path = "app/xeyes-1.1.1.tar.gz"

    version('1.1.1', sha256='3a1871a560ab87c72a2e2ecb7fd582474448faec3e254c9bd8bead428ab1bca3')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxext')
    depends_on('libxmu')
    depends_on('libxrender@0.4:')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
