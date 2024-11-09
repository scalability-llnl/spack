# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsetroot(AutotoolsPackage, XorgPackage):
    """xsetroot - root window parameter setting utility for X."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xsetroot"
    xorg_mirror_path = "app/xsetroot-1.1.1.tar.gz"

    license("MIT")

    version("1.1.3", sha256="80dbb0d02807e89294a042298b8a62f9aa0c3a94d89244ccbc35e4cf80fcaaba")
    version("1.1.2", sha256="9d007f5119be09924ac3a5d2bd506f32e6c164b82633c88d2aff26311e1a2a2b")
    version("1.1.1", sha256="6cdd48757d18835251124138b4a8e4008c3bbc51cf92533aa39c6ed03277168b")

    depends_on("c", type="build")

    depends_on("libxmu")
    depends_on("libx11")
    depends_on("libxcursor")

    depends_on("xbitmaps")
    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
