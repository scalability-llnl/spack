# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxxf86dga(AutotoolsPackage, XorgPackage):
    """libXxf86dga - Client library for the XFree86-DGA extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXxf86dga"
    xorg_mirror_path = "lib/libXxf86dga-1.1.4.tar.gz"

    version('1.1.4', sha256='e6361620a15ceba666901ca8423e8be0c6ed0271a7088742009160349173766b')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('xf86dgaproto@2.0.99.2:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
