# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxext(AutotoolsPackage, XorgPackage):
    """libXext - library for common extensions to the X11 protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXext"
    xorg_mirror_path = "lib/libXext-1.3.3.tar.gz"

    version('1.3.3', sha256='eb0b88050491fef4716da4b06a4d92b4fc9e76f880d6310b2157df604342cfe5')

    depends_on('libx11@1.6:')

    depends_on('xproto@7.0.13:')
    depends_on('xextproto@7.1.99:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    @property
    def libs(self):
        return find_libraries('libXext', self.prefix,
                              shared=True, recursive=True)
