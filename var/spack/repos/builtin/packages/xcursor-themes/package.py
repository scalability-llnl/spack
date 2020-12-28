# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcursorThemes(Package, XorgPackage):
    """This is a default set of cursor themes for use with libXcursor,
    originally created for the XFree86 Project, and now shipped as part
    of the X.Org software distribution."""

    homepage = "http://cgit.freedesktop.org/xorg/data/cursors"
    xorg_mirror_path = "data/xcursor-themes-1.0.4.tar.gz"

    version('1.0.4', sha256='8ed23bab13a4010fe4e95b37eefb634e31ac7cb8240b8b3b7d919c3a2db09503')

    depends_on('libxcursor')

    depends_on('xcursorgen', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))

        make()
        make('install')

        # `make install` copies the files to the libxcursor installation.
        # Create a fake directory to convince Spack that we actually
        # installed something.
        mkdir(prefix.lib)
