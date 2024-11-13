# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xkill(AutotoolsPackage, XorgPackage):
    """xkill is a utility for forcing the X server to close connections to
    clients.  This program is very dangerous, but is useful for aborting
    programs that have displayed undesired windows on a user's screen."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xkill"
    xorg_mirror_path = "app/xkill-1.0.4.tar.gz"

    license("MIT")

    version("1.0.6", sha256="3b35a2f4b67dda1e98b6541488cd7f7343eb6e3dbe613aeff3d5a5a4c4c64b58")
    version("1.0.5", sha256="98fab8a8af78d5aae4e1f284b580c60e3d25ed2a72daa4dbce419b28d8adaf8a")
    version("1.0.4", sha256="f80115f2dcca3d4b61f3c28188752c21ca7b2718b54b6e0274c0497a7f827da0")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxmu")

    depends_on("xproto@7.0.22:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
