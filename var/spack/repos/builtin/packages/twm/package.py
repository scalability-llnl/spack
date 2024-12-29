# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Twm(AutotoolsPackage, XorgPackage):
    """twm is a window manager for the X Window System.  It provides
    titlebars, shaped windows, several forms of icon management,
    user-defined macro functions, click-to-type and pointer-driven
    keyboard focus, and user-specified key and pointer button bindings."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/twm"
    xorg_mirror_path = "app/twm-1.0.9.tar.gz"

    license("MIT")

    version("1.0.12", sha256="4150c9ec595520167ab8c4efcb5cf82641a4c4db78ce0a1cb4834e6aeb7c87fb")
    version("1.0.11", sha256="410ecabac54e6db7afd5c20a78d89c0134f3c74b149bee71b1fec775e6e060cc")
    version("1.0.10", sha256="679a1d07078c918fa32454498dc15573b299bbb0f001499e213c408e4b2170f5")
    version("1.0.9", sha256="1c325e8456a200693c816baa27ceca9c5e5e0f36af63d98f70a335853a0039e8")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")
    depends_on("libxt")
    depends_on("libxmu")
    depends_on("libice")
    depends_on("libsm")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
