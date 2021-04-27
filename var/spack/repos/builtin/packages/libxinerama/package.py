# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxinerama(AutotoolsPackage, XorgPackage):
    """libXinerama - API for Xinerama extension to X11 Protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXinerama"
    xorg_mirror_path = "lib/libXinerama-1.1.3.tar.gz"

    version('1.1.3', sha256='0ba243222ae5aba4c6a3d7a394c32c8b69220a6872dbb00b7abae8753aca9a44')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto')
    depends_on('xineramaproto@1.1.99.1:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    @property
    def libs(self):
        return find_libraries('libXinerama', self.prefix,
                              shared=True, recursive=True)
