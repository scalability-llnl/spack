# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfontsel(AutotoolsPackage, XorgPackage):
    """xfontsel application provides a simple way to display the X11 core
    protocol fonts known to your X server, examine samples of each, and
    retrieve the X Logical Font Description ("XLFD") full name for a font."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfontsel"
    xorg_mirror_path = "app/xfontsel-1.0.5.tar.gz"

    version('1.0.5', sha256='9b3ad0cc274398d22be9fa7efe930f4e3749fd4b1b61d9c31a7fb6c1f1ff766e')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
