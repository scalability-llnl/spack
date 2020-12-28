# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlogo(AutotoolsPackage, XorgPackage):
    """The xlogo program simply displays the X Window System logo."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlogo"
    xorg_mirror_path = "app/xlogo-1.0.4.tar.gz"

    version('1.0.4', sha256='0072eb3b41af77d5edfafb12998c7dd875f2795dc94735a998fd2ed8fc246e57')

    depends_on('libsm')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.0:')
    depends_on('libxext')
    depends_on('libx11')
    depends_on('libxft')
    depends_on('libxrender')
    depends_on('libxt')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
