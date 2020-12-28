# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxau(AutotoolsPackage, XorgPackage):
    """The libXau package contains a library implementing the X11
    Authorization Protocol. This is useful for restricting client
    access to the display."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXau/"
    xorg_mirror_path = "lib/libXau-1.0.8.tar.gz"

    version('1.0.8', sha256='c343b4ef66d66a6b3e0e27aa46b37ad5cab0f11a5c565eafb4a1c7590bc71d7b')

    depends_on('xproto', type=('build', 'link'))
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
