# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfsinfo(AutotoolsPackage, XorgPackage):
    """xfsinfo is a utility for displaying information about an X font
    server.  It is used to examine the capabilities of a server, the
    predefined values for various parameters used in communicating between
    clients and the server, and the font catalogues and alternate servers
    that are available."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xfsinfo"
    xorg_mirror_path = "app/xfsinfo-1.0.5.tar.gz"

    version("1.0.7", sha256="df874933710c9c38640496a2121d73272501b9620bdb95784e9e67b913788151")
    version("1.0.6", sha256="a817e553703748fe2d721b1fe8ea95687ee78f7aef25427ed72d9584494d91e1")
    version("1.0.5", sha256="56a0492ed2cde272dc8f4cff4ba0970ccb900e51c10bb8ec62747483d095fd69")

    depends_on("c", type="build")

    depends_on("libfs")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
