# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class I3(AutotoolsPackage):
    """i3, improved tiling wm. i3 is a tiling window manager, completely
    written from scratch. The target platforms are GNU/Linux and BSD operating
    systems, our code is Free and Open Source Software (FOSS) under the BSD
    license. i3 is primarily targeted at advanced users and developers."""

    homepage = "https://i3wm.org/"
    url = "https://github.com/i3/i3/archive/4.14.1.tar.gz"

    license("BSD-3-Clause")

    version("4.14.1", sha256="28d8102d656f17445a6e1523b12c1a730cc3925a520add1f75b56b9c842932f9")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libev")
    depends_on("startup-notification")
    depends_on("xcb-util-cursor")
    depends_on("xcb-util-keysyms")
    depends_on("xcb-util-wm")
    depends_on("xcb-util-xrm")
    depends_on("libxkbcommon")
    depends_on("yajl")
    depends_on("cairo+X")
    depends_on("pango+X")
