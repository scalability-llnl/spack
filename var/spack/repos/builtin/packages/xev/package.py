# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xev(AutotoolsPackage, XorgPackage):
    """xev creates a window and then asks the X server to send it X11 events
    whenever anything happens to the window (such as it being moved,
    resized, typed in, clicked in, etc.).  You can also attach it to an
    existing window.  It is useful for seeing what causes events to occur
    and to display the information that they contain; it is essentially a
    debugging and development tool, and should not be needed in normal
    usage."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xev"
    xorg_mirror_path = "app/xev-1.2.2.tar.gz"

    version('1.2.2', sha256='e4c0c7b6f411e8b9731f2bb10d729d167bd00480d172c28b62607a6ea9e45c57')

    depends_on('libxrandr@1.2:')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
