# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcalc(AutotoolsPackage, XorgPackage):
    """xcalc is a scientific calculator X11 client that can emulate a TI-30
    or an HP-10C."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xcalc"
    xorg_mirror_path = "app/xcalc-1.0.6.tar.gz"

    version('1.0.6', sha256='7fd5cd9a35160925c41cbadfb1ea23599fa20fd26cd873dab20a650b24efe8d1')

    depends_on('libxaw')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
