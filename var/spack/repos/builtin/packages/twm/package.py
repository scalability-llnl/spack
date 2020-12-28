# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Twm(AutotoolsPackage, XorgPackage):
    """twm is a window manager for the X Window System.  It provides
    titlebars, shaped windows, several forms of icon management,
    user-defined macro functions, click-to-type and pointer-driven
    keyboard focus, and user-specified key and pointer button bindings."""

    homepage = "http://cgit.freedesktop.org/xorg/app/twm"
    xorg_mirror_path = "app/twm-1.0.9.tar.gz"

    version('1.0.9', sha256='1c325e8456a200693c816baa27ceca9c5e5e0f36af63d98f70a335853a0039e8')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libice')
    depends_on('libsm')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
