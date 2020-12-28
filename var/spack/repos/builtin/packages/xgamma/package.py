# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xgamma(AutotoolsPackage, XorgPackage):
    """xgamma allows X users to query and alter the gamma correction of a
    monitor via the X video mode extension (XFree86-VidModeExtension)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xgamma"
    xorg_mirror_path = "app/xgamma-1.0.6.tar.gz"

    version('1.0.6', sha256='66da1d67e84146518b69481c6283c5d8f1027ace9ff7e214d3f81954842e796a')

    depends_on('libx11')
    depends_on('libxxf86vm')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
