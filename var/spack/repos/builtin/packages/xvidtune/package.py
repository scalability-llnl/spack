# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xvidtune(AutotoolsPackage, XorgPackage):
    """xvidtune is a client interface to the X server video mode
    extension (XFree86-VidModeExtension)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xvidtune"
    xorg_mirror_path = "app/xvidtune-1.0.3.tar.gz"

    version('1.0.3', sha256='c0e158388d60e1ce054ce462958a46894604bd95e13093f3476ec6d9bbd786d4')

    depends_on('libxxf86vm')
    depends_on('libxt')
    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
