# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdm(AutotoolsPackage, XorgPackage):
    """X Display Manager / XDMCP server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xdm"
    xorg_mirror_path = "app/xdm-1.1.11.tar.gz"

    version('1.1.11', sha256='38c544a986143b1f24566c1a0111486b339b92224b927be78714eeeedca12a14')

    depends_on('libxmu')
    depends_on('libx11')
    depends_on('libxau')
    depends_on('libxinerama')
    depends_on('libxft')
    depends_on('libxpm')
    depends_on('libxaw')
    depends_on('libxdmcp')
    depends_on('libxt')
    depends_on('libxext')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
