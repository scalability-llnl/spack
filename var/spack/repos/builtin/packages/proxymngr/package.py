# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Proxymngr(AutotoolsPackage, XorgPackage):
    """The proxy manager (proxymngr) is responsible for resolving requests from
    xfindproxy (and other similar clients), starting new proxies when
    appropriate, and keeping track of all of the available proxy services.
    The proxy manager strives to reuse existing proxies whenever possible."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/proxymngr"
    xorg_mirror_path = "app/proxymngr-1.0.4.tar.gz"

    version("1.0.4", sha256="d40f2d15985ee8e8ef5320a85c0b1899a7bc95974a65137ae886e499bced86f4")

    depends_on("c", type="build")

    depends_on("libice")
    depends_on("libxt")
    depends_on("lbxproxy")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("xproxymanagementprotocol", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
