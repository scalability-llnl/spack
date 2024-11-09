# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxtrap(AutotoolsPackage, XorgPackage):
    """libXTrap is the Xlib-based client API for the DEC-XTRAP extension.

    XTrap was a proposed standard extension for X11R5 which facilitated the
    capturing of server protocol and synthesizing core input events.

    Digital participated in the X Consortium's xtest working group which chose
    to evolve XTrap functionality into the XTEST & RECORD extensions for X11R6.

    As X11R6 was released in 1994, XTrap has now been deprecated for over
    15 years, and uses of it should be quite rare."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXTrap"
    xorg_mirror_path = "lib/libXTrap-1.0.1.tar.gz"

    version("1.0.1", sha256="db748e299dcc9af68428795b898a4a96cf806f79b75786781136503e4fce5e17")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")

    depends_on("trapproto", type=("build", "link"))
    depends_on("xextproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
