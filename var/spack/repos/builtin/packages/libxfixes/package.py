# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfixes(AutotoolsPackage, XorgPackage):
    """This package contains header files and documentation for the XFIXES
    extension.  Library and server implementations are separate."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXfixes"
    xorg_mirror_path = "lib/libXfixes-5.0.2.tar.gz"

    version('5.0.2', sha256='ad8df1ecf3324512b80ed12a9ca07556e561b14256d94216e67a68345b23c981')

    depends_on('libx11@1.6:')

    depends_on('xproto', type='build')
    depends_on('fixesproto@5.0:', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
