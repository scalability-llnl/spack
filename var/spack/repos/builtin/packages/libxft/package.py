# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxft(AutotoolsPackage, XorgPackage):
    """X FreeType library.

    Xft version 2.1 was the first stand alone release of Xft, a library that
    connects X applications with the FreeType font rasterization library. Xft
    uses fontconfig to locate fonts so it has no configuration files."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXft"
    xorg_mirror_path = "lib/libXft-2.3.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("2.3.8", sha256="32e48fe2d844422e64809e4e99b9d8aed26c1b541a5acf837c5037b8d9f278a8")
    version("2.3.7", sha256="75b4378644f5df3a15f684f8f0b5ff1324d37aacd5a381f3b830a2fbe985f660")
    version("2.3.6", sha256="b7e59f69e0bbabe9438088775f7e5a7c16a572e58b11f9722519385d38192df5")
    version("2.3.5", sha256="f7324aa0664115223672bae55086f3a9ae8f6ad4cdca87a8dd620295ee459e1a")
    version("2.3.4", sha256="1eca71bec9cb483165ce1ab94f5cd3036269f5268651df6a2d99c4a7ab644d79")
    version("2.3.3", sha256="3c3cf88b1a96e49a3d87d67d9452d34b6e25e96ae83959b8d0a980935014d701")
    version("2.3.2", sha256="26cdddcc70b187833cbe9dc54df1864ba4c03a7175b2ca9276de9f05dce74507")

    depends_on("c", type="build")  # generated

    depends_on("freetype@2.1.6:")
    depends_on("fontconfig@2.5.92:")
    depends_on("libx11")
    depends_on("libxrender@0.8.2:")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
