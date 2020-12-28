# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xvinfo(AutotoolsPackage, XorgPackage):
    """xvinfo prints out the capabilities of any video adaptors associated
    with the display that are accessible through the X-Video extension."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xvinfo"
    xorg_mirror_path = "app/xvinfo-1.1.3.tar.gz"

    version('1.1.3', sha256='1c1c2f97abfe114389e94399cc7bf3dfd802ed30ad41ba23921d005bd8a6c39f')

    depends_on('libxv')
    depends_on('libx11')

    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
