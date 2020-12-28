# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xkbprint(AutotoolsPackage, XorgPackage):
    """xkbprint generates a printable or encapsulated PostScript description
    of an XKB keyboard description."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xkbprint"
    xorg_mirror_path = "app/xkbprint-1.0.4.tar.gz"

    version('1.0.4', sha256='169ebbf57fc8b7685c577c73a435998a38c27e0d135ce0a55fccc64cbebec768')

    depends_on('libxkbfile')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
