# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwud(AutotoolsPackage, XorgPackage):
    """xwud allows X users to display in a window an image saved in a
    specially formatted dump file, such as produced by xwd."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xwud"
    xorg_mirror_path = "app/xwud-1.0.4.tar.gz"

    version('1.0.4', sha256='b7c124ccd87f529daedb7ef01c670ce6049fe141fd9ba7f444361de34510cd6c')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
