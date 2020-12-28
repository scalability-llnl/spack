# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Oclock(AutotoolsPackage, XorgPackage):
    """oclock is a simple analog clock using the SHAPE extension to make
    a round (possibly transparent) window."""

    homepage = "http://cgit.freedesktop.org/xorg/app/oclock"
    xorg_mirror_path = "app/oclock-1.0.3.tar.gz"

    version('1.0.3', sha256='6628d1abe1612b87db9d0170cbe7f1cf4205cd764274f648c3c1bdb745bff877')

    depends_on('libx11')
    depends_on('libxmu')
    depends_on('libxext')
    depends_on('libxt')
    depends_on('libxkbfile')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
