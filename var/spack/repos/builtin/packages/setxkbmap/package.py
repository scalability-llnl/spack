# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Setxkbmap(AutotoolsPackage, XorgPackage):
    """setxkbmap is an X11 client to change the keymaps in the X server for a
    specified keyboard to use the layout determined by the options listed
    on the command line."""

    homepage = "http://cgit.freedesktop.org/xorg/app/setxkbmap"
    xorg_mirror_path = "app/setxkbmap-1.3.1.tar.gz"

    version('1.3.1', sha256='e24a73669007fa3b280eba4bdc7f75715aeb2e394bf2d63f5cc872502ddde264')

    depends_on('libxkbfile')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
