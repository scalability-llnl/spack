# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfontenc(AutotoolsPackage, XorgPackage):
    """libfontenc - font encoding library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libfontenc"
    xorg_mirror_path = "lib/libfontenc-1.1.3.tar.gz"

    version('1.1.3', sha256='6fba26760ca8d5045f2b52ddf641c12cedc19ee30939c6478162b7db8b6220fb')

    depends_on('zlib')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
