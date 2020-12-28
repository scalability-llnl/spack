# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfwp(AutotoolsPackage, XorgPackage):
    """xfwp proxies X11 protocol connections, such as through a firewall."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfwp"
    xorg_mirror_path = "app/xfwp-1.0.3.tar.gz"

    version('1.0.3', sha256='6fe243bde0374637e271a3f038b5d6d79a04621fc18162727782392069c5c04d')

    depends_on('libice')

    depends_on('xproto', type='build')
    depends_on('xproxymanagementprotocol', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    # FIXME: fails with the error message:
    # io.c:1039:7: error: implicit declaration of function 'swab'
