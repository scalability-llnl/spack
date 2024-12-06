# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdriinfo(AutotoolsPackage, XorgPackage):
    """xdriinfo - query configuration information of X11 DRI drivers."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xdriinfo"
    xorg_mirror_path = "app/xdriinfo-1.0.5.tar.gz"

    license("custom")

    version("1.0.7", sha256="9fab95510b1f67409632fb8af01369b128f4d12763fe1a2662f5666976a7d30c")
    version("1.0.6", sha256="c59d1d97d8b1066ea470407237c87fb131ca9f6c4db4652a6e9461ae03c698ad")
    version("1.0.5", sha256="e4e6abaa4591c540ab63133927a6cebf0a5f4d27dcd978878ab4a422d62a838e")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("expat")
    depends_on("libxshmfence")
    depends_on("libxext")
    depends_on("libxdamage")
    depends_on("libxfixes")
    depends_on("pcre")

    # Uses glXGetProcAddressARB, add OpenGL:
    depends_on("gl")
    depends_on("glproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
