# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iceauth(AutotoolsPackage, XorgPackage):
    """The iceauth program is used to edit and display the authorization
    information used in connecting with ICE.   It operates very much
    like the xauth program for X11 connection authentication records."""

    homepage = "http://cgit.freedesktop.org/xorg/app/iceauth"
    xorg_mirror_path = "app/iceauth-1.0.7.tar.gz"

    version('1.0.7', sha256='6c9706cce276609876e768759ed4ee3b447cd17af4a61f9b5a374c7dda9696d8')

    depends_on('libice')

    depends_on('xproto@7.0.22:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
