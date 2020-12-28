# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxaw(AutotoolsPackage, XorgPackage):
    """Xaw is the X Athena Widget Set.
    Xaw is a widget set based on the X Toolkit Intrinsics (Xt) Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXaw"
    xorg_mirror_path = "lib/libXaw-1.0.13.tar.gz"

    version('1.0.13', sha256='7e74ac3e5f67def549722ff0333d6e6276b8becd9d89615cda011e71238ab694')
    version('1.0.12', sha256='e32abc68d759ffb643f842329838f8b6c157e31023cc91059aabf730e7222ad2')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libxpm')

    depends_on('xproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
