# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xpr(AutotoolsPackage, XorgPackage):
    """xpr takes as input a window dump file produced by xwd
    and formats it for output on various types of printers."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xpr"
    xorg_mirror_path = "app/xpr-1.0.4.tar.gz"

    version('1.0.4', sha256='9ec355388ae363fd40239a3fa56908bb2f3e53b5bfc872cf0182d14d730c6207')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
