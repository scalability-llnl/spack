# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bdftopcf(AutotoolsPackage, XorgPackage):
    """bdftopcf is a font compiler for the X server and font server.  Fonts
    in Portable Compiled Format can be read by any architecture, although
    the file is structured to allow one particular architecture to read
    them directly without reformatting.  This allows fast reading on the
    appropriate machine, but the files are still portable (but read more
    slowly) on other machines."""

    homepage = "http://cgit.freedesktop.org/xorg/app/bdftopcf"
    xorg_mirror_path = "app/bdftopcf-1.0.5.tar.gz"

    version('1.0.5', sha256='78a5ec945de1d33e6812167b1383554fda36e38576849e74a9039dc7364ff2c3')

    depends_on('libxfont')

    depends_on('pkgconfig', type='build')
    depends_on('xproto', type='build')
    depends_on('fontsproto', type='build')
    depends_on('util-macros', type='build')
