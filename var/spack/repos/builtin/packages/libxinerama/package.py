# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxinerama(AutotoolsPackage, XorgPackage):
    """libXinerama - API for Xinerama extension to X11 Protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXinerama"
    xorg_mirror_path = "lib/libXinerama-1.1.3.tar.gz"

    version('1.1.3', sha256='0ba243222ae5aba4c6a3d7a394c32c8b69220a6872dbb00b7abae8753aca9a44')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('xineramaproto@1.1.99.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
