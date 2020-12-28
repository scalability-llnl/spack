# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xrdb(AutotoolsPackage, XorgPackage):
    """xrdb - X server resource database utility."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrdb"
    xorg_mirror_path = "app/xrdb-1.1.0.tar.gz"

    version('1.1.0', sha256='44b0b6b7b7eb80b83486dfea67c880f6b0059052386c7ddec4d58fd2ad9ae8e9')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
