# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xbitmaps(AutotoolsPackage, XorgPackage):
    """The xbitmaps package contains bitmap images used by multiple
    applications built in Xorg."""

    homepage = "https://cgit.freedesktop.org/xorg/data/bitmaps/"
    xorg_mirror_path = "data/xbitmaps-1.1.1.tar.gz"

    version('1.1.1', sha256='3bc89e05be4179ce4d3dbba1ae554da4591d41f7a489d9e2735a18cfd8378188')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
