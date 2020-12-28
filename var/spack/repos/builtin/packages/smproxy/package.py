# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Smproxy(AutotoolsPackage, XorgPackage):
    """smproxy allows X applications that do not support X11R6 session
    management to participate in an X11R6 session."""

    homepage = "http://cgit.freedesktop.org/xorg/app/smproxy"
    xorg_mirror_path = "app/smproxy-1.0.6.tar.gz"

    version('1.0.6', sha256='a01374763426a5fdcbc7a65edc54e2070cdbca4df41dddd3051c7586e4c814c9')

    depends_on('libsm')
    depends_on('libice')
    depends_on('libxt')
    depends_on('libxmu')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
