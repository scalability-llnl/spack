# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xstdcmap(AutotoolsPackage, XorgPackage):
    """The xstdcmap utility can be used to selectively define standard colormap
    properties.  It is intended to be run from a user's X startup script to
    create standard colormap definitions in order to facilitate sharing of
    scarce colormap resources among clients using PseudoColor visuals."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xstdcmap"
    xorg_mirror_path = "app/xstdcmap-1.0.3.tar.gz"

    version('1.0.3', sha256='b97aaa883a9eedf9c3056ea1a7e818e3d93b63aa1f54193ef481d392bdef5711')

    depends_on('libxmu')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
