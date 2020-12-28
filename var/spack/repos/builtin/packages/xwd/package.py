# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwd(AutotoolsPackage, XorgPackage):
    """xwd - dump an image of an X window."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xwd"
    xorg_mirror_path = "app/xwd-1.0.6.tar.gz"

    version('1.0.6', sha256='ff01f0a4b736f955aaf7c8c3942211bc52f9fb75d96f2b19777f33fff5dc5b83')

    depends_on('libx11')
    depends_on('libxkbfile')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
