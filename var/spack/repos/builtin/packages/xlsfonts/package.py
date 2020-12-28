# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlsfonts(AutotoolsPackage, XorgPackage):
    """xlsfonts lists fonts available from an X server via the X11
    core protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlsfonts"
    xorg_mirror_path = "app/xlsfonts-1.0.5.tar.gz"

    version('1.0.5', sha256='2a7aeca1023a3918ad2a1af2258ed63d8f8b6c48e53841b3a3f15fb9a0c008ce')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
