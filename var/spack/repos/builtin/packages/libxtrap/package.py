# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxtrap(AutotoolsPackage):
    """libXTrap is the Xlib-based client API for the DEC-XTRAP extension.

    XTrap was a proposed standard extension for X11R5 which facilitated the
    capturing of server protocol and synthesizing core input events.

    Digital participated in the X Consortium's xtest working group which chose
    to evolve XTrap functionality into the XTEST & RECORD extensions for X11R6.

    As X11R6 was released in 1994, XTrap has now been deprecated for over
    15 years, and uses of it should be quite rare."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXTrap"
    url      = "https://www.x.org/archive/individual/lib/libXTrap-1.0.1.tar.gz"

    version('1.0.1', 'fde266b82ee14da3e4f4f81c9584c1ea')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxext')

    depends_on('trapproto', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
