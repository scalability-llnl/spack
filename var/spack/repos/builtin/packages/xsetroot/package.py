# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsetroot(AutotoolsPackage, XorgPackage):
    """xsetroot - root window parameter setting utility for X."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xsetroot"
    xorg_mirror_path = "app/xsetroot-1.1.1.tar.gz"

    version('1.1.1', sha256='6cdd48757d18835251124138b4a8e4008c3bbc51cf92533aa39c6ed03277168b')

    depends_on('libxmu')
    depends_on('libx11')
    depends_on('libxcursor')

    depends_on('xbitmaps', type='build')
    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
