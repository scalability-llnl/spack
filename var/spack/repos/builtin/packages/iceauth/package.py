# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iceauth(AutotoolsPackage, XorgPackage):
    """The iceauth program is used to edit and display the authorization
    information used in connecting with ICE.   It operates very much
    like the xauth program for X11 connection authentication records."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/iceauth"
    xorg_mirror_path = "app/iceauth-1.0.7.tar.gz"

    license("MIT")

    version("1.0.10", sha256="f17f373c6e7bfef9cfa4c688f165dfebec7642ad7c6304c5bb3c9bc2bfcde747")
    version("1.0.9", sha256="5ca274cf210453e7d7cf5c827a2fbc92149df83824f99a27cde17e1f20324dc6")
    version("1.0.7", sha256="6c9706cce276609876e768759ed4ee3b447cd17af4a61f9b5a374c7dda9696d8")

    depends_on("c", type="build")

    depends_on("libice")

    depends_on("xproto@7.0.22:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
