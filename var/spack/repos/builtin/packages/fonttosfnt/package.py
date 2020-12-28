# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fonttosfnt(AutotoolsPackage, XorgPackage):
    """Wrap a bitmap font in a sfnt (TrueType) wrapper."""

    homepage = "http://cgit.freedesktop.org/xorg/app/fonttosfnt"
    xorg_mirror_path = "app/fonttosfnt-1.0.4.tar.gz"

    version('1.0.4', sha256='3873636be5b3b8e4160070e8f9a7a9221b5bd5efbf740d7abaa9092e10732673')

    depends_on('freetype')
    depends_on('libfontenc')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
