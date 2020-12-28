# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcomposite(AutotoolsPackage, XorgPackage):
    """libXcomposite - client library for the Composite extension to the
    X11 protocol."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXcomposite"
    xorg_mirror_path = "lib/libXcomposite-0.4.4.tar.gz"

    version('0.4.4', sha256='83c04649819c6f52cda1b0ce8bcdcc48ad8618428ad803fb07f20b802f1bdad1')

    depends_on('libx11')
    depends_on('libxfixes')
    depends_on('fixesproto@0.4:', type='build')
    depends_on('compositeproto@0.4:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
