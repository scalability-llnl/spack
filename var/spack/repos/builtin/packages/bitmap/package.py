# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bitmap(AutotoolsPackage, XorgPackage):
    """bitmap, bmtoa, atobm - X bitmap (XBM) editor and converter utilities."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/bitmap"
    xorg_mirror_path = "app/bitmap-1.0.8.tar.gz"

    version("1.1.1", sha256="86928020ece030435eb5ae795a5f22c5ca0886a6c589187886d1b6d14d9eec81")
    version("1.1.0", sha256="60ca941e8e38e1f8f9c61d3e86c098878113fd11eac4e07177c111f0bf00779e")
    version("1.0.8", sha256="1a2fbd10a2ca5cd93f7b77bbb0555b86d8b35e0fc18d036b1607c761755006fc")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxmu")
    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt")

    depends_on("xbitmaps")
    depends_on("xproto@7.0.25:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
