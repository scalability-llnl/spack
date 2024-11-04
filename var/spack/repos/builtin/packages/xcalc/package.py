# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcalc(AutotoolsPackage, XorgPackage):
    """xcalc is a scientific calculator X11 client that can emulate a TI-30
    or an HP-10C."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xcalc"
    xorg_mirror_path = "app/xcalc-1.0.6.tar.gz"

    license("MIT")

    version("1.1.1", sha256="9219c889bfb2d0e168ef9a14700662c5cde829b69b12875cb6d59b70d4b68f3b")
    version("1.1.0", sha256="a86418d9af9d0e57e5253ba1c29e754480509c828d369aaaca48400b2045e630")
    version("1.0.7", sha256="2b00129583f51a45acfcaaa461750169e530996e190b31f7a92891846380f1f5")
    version("1.0.6", sha256="7fd5cd9a35160925c41cbadfb1ea23599fa20fd26cd873dab20a650b24efe8d1")

    depends_on("c", type="build")

    depends_on("libxaw")
    depends_on("libxt")
    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
