# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xprop(AutotoolsPackage, XorgPackage):
    """xprop is a command line tool to display and/or set window and font
    properties of an X server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xprop"
    xorg_mirror_path = "app/xprop-1.2.2.tar.gz"

    version('1.2.2', sha256='3db78771ce8fb8954fb242ed9d4030372523649c5e9c1a9420340020dd0afbc2')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
