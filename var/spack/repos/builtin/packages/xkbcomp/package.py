# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xkbcomp(AutotoolsPackage, XorgPackage):
    """The X Keyboard (XKB) Extension essentially replaces the core protocol
    definition of a keyboard. The extension makes it possible to specify
    clearly and explicitly most aspects of keyboard behaviour on a per-key
    basis, and to track more closely the logical and physical state of a
    keyboard. It also includes a number of keyboard controls designed to
    make keyboards more accessible to people with physical impairments."""

    homepage = "https://www.x.org/wiki/XKB/"
    xorg_mirror_path = "app/xkbcomp-1.3.1.tar.gz"

    version('1.4.4', sha256='159fba6b62ef4a3fb16ef7fc4eb4fc26f3888652471ceb604c495783dda020bc')
    version('1.3.1', sha256='018e83a922430652d4bc3f3db610d2296e618c76c9b3fbcdccde975aeb655749')

    depends_on('libx11')
    depends_on('libxkbfile')

    depends_on('xproto@7.0.17:')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
