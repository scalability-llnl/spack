# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpaper(AutotoolsPackage):
    """The paper library and accompanying files are intended to provide a
    simple way for applications to take actions based on a system- or
    user-specified paper size."""

    homepage = "https://packages.debian.org/unstable/source/libpaper"
    url      = "http://deb.debian.org/debian/pool/main/libp/libpaper/libpaper_1.1.28.tar.gz"

    version('1.1.28', sha256='c8bb946ec93d3c2c72bbb1d7257e90172a22a44a07a07fb6b802a5bb2c95fddc')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
