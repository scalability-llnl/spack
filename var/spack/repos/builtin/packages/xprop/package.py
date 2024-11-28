# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xprop(AutotoolsPackage, XorgPackage):
    """xprop is a command line tool to display and/or set window and font
    properties of an X server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xprop"
    xorg_mirror_path = "app/xprop-1.2.2.tar.gz"

    license("MIT")

    version("1.2.7", sha256="11c06a876b0aa0bfac6cbfe4b3ebe1f5062f8b39b9b1b6c136a8629265f134b6")
    version("1.2.6", sha256="58ee5ee0c47fa454d3b16312e778c3f549605a8ad0fd0daafc70d2d6174b116d")
    version("1.2.5", sha256="b7bf6b6be6cf23e7966a153fc84d5901c14f01ee952fbd9d930aa48e2385d670")
    version("1.2.4", sha256="dddb6e208ffa515e68f001c22077a465f1365a4bcf91d9b37f336a6c0d15400d")
    version("1.2.3", sha256="82c13f40577e10b6f3f0160a21b1e46c00a0c719aa560618b961c453e1b5c80d")
    version("1.2.2", sha256="3db78771ce8fb8954fb242ed9d4030372523649c5e9c1a9420340020dd0afbc2")

    depends_on("c", type="build")

    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
