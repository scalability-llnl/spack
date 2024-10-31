# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Viewres(AutotoolsPackage, XorgPackage):
    """viewres displays a tree showing the widget class hierarchy of the
    Athena Widget Set (libXaw)."""

    homepage = "https://cgit.freedesktop.org/xorg/app/viewres"
    xorg_mirror_path = "app/viewres-1.0.4.tar.gz"

    license("X11")

    version("1.0.7", sha256="5dd63ee19575dd1d40360242ecc1ff96e222d9b80a2b7b8b89e6d1e0f2367d78")
    version("1.0.6", sha256="2c9f1892dbb5563b704fd06f45cd9d263d8176027033d8438c79a2ceddac200f")
    version("1.0.5", sha256="9dee5e6b0a18961bb5c33f3f654605d45912087b6ba781cb2277d1941fa35a4b")
    version("1.0.4", sha256="fd2aaec85c952fd6984fe14d0fcbda4d2ab9849a9183e4787b0ef552a10a87a1")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
