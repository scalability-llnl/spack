# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfindproxy(AutotoolsPackage, XorgPackage):
    """xfindproxy is used to locate available X11 proxy services.

    It utilizes the Proxy Management Protocol to communicate with a proxy
    manager.  The proxy manager keeps track of all available proxy
    services, starts new proxies when necessary, and makes sure that
    proxies are shared whenever possible."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xfindproxy"
    xorg_mirror_path = "app/xfindproxy-1.0.4.tar.gz"

    version("1.0.4", sha256="fa6152fcf9c16fbb2ef52259731df5df899a39a86894b0508456613f26ff924a")

    depends_on("c", type="build")

    depends_on("libice")
    depends_on("libxt")

    depends_on("xproto", type="build")
    depends_on("xproxymanagementprotocol", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
