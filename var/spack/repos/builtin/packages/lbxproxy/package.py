# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lbxproxy(AutotoolsPackage, XorgPackage):
    """lbxproxy accepts client connections, multiplexes them over a single
    connection to the X server, and performs various optimizations on the
    X protocol to make it faster over low bandwidth and/or high latency
    connections.

    Note that the X server source from X.Org no longer supports the LBX
    extension, so this program is only useful in connecting to older
    X servers."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/lbxproxy"
    xorg_mirror_path = "app/lbxproxy-1.0.3.tar.gz"

    version("1.0.3", sha256="db36251c9656c7da720f31e10df384f8946a9a5395915371b60d9423ad8f6a80")

    depends_on("c", type="build")

    depends_on("libxext")
    depends_on("liblbxutil")
    depends_on("libx11")
    depends_on("libice")

    depends_on("xtrans")
    depends_on("xproxymanagementprotocol", type="build")
    depends_on("bigreqsproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
