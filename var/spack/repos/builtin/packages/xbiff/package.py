# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xbiff(AutotoolsPackage, XorgPackage):
    """xbiff provides graphical notification of new e-mail.
    It only handles mail stored in a filesystem accessible file,
    not via IMAP, POP or other remote access protocols."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xbiff"
    xorg_mirror_path = "app/xbiff-1.0.3.tar.gz"

    version('1.0.3', sha256='b4b702348674985741685e3ec7fcb5640ffb7bf20e753fc2d708f70f2e4c304d')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxext')
    depends_on('libx11')

    depends_on('xbitmaps', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
