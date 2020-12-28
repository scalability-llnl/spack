# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Busybox(MakefilePackage):
    """BusyBox combines tiny versions of many common UNIX utilities into
    a single small executable. It provides replacements for most of
    the utilities you usually find in GNU fileutils, shellutils, etc"""

    homepage = "https://busybox.net"
    url      = "https://busybox.net/downloads/busybox-1.31.0.tar.bz2"

    version('1.31.1', sha256='d0f940a72f648943c1f2211e0e3117387c31d765137d92bd8284a3fb9752a998')
    version('1.31.0', sha256='0e4925392fd9f3743cc517e031b68b012b24a63b0cf6c1ff03cce7bb3846cc99')
    version('1.30.1', sha256='3d1d04a4dbd34048f4794815a5c48ebb9eb53c5277e09ffffc060323b95dfbdc')
    version('1.30.0', sha256='9553da068c0a30b1b8b72479908c1ba58672e2be7b535363a88de5e0f7bc04ce')

    def build(self, spec, prefix):
        make('defconfig')
        make()

    def install(self, spec, prefix):
        make('install')
        install_tree('.', prefix)
