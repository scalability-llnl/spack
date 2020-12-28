# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xedit(AutotoolsPackage, XorgPackage):
    """Xedit is a simple text editor for X."""

    homepage = "https://cgit.freedesktop.org/xorg/app/xedit"
    xorg_mirror_path = "app/xedit-1.2.2.tar.gz"

    version('1.2.2', sha256='7e2dacbc2caed81d462ee028e108866893217d55e35e4b860b09be2b409ee18f')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt@1.0:')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
