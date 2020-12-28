# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xinit(AutotoolsPackage, XorgPackage):
    """The xinit program is used to start the X Window System server and a
    first client program on systems that are not using a display manager
    such as xdm."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xinit"
    xorg_mirror_path = "app/xinit-1.3.4.tar.gz"

    version('1.3.4', sha256='754c284875defa588951c1d3d2b20897d3b84918d0a97cb5a4724b00c0da0746')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
