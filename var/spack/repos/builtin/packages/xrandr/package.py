# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xrandr(AutotoolsPackage, XorgPackage):
    """xrandr - primitive command line interface to X11 Resize, Rotate, and
    Reflect (RandR) extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xrandr"
    xorg_mirror_path = "app/xrandr-1.5.0.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.5.2", sha256="efd062cd228dc18a7de26422c81bc4be6a7e62f7f0ad6f9bebdd9ff8385c5668")
    version("1.5.1", sha256="7b99edb7970a1365eaf5bcaf552144e4dfc3ccf510c4abc08569849929fb366e")
    version("1.5.0", sha256="ddfe8e7866149c24ccce8e6aaa0623218ae19130c2859cadcaa4228d8bb4a46d")

    depends_on("c", type="build")

    depends_on("libxrandr@1.5:")
    depends_on("libxrender")
    depends_on("libx11")
    depends_on("randrproto", type="build")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
