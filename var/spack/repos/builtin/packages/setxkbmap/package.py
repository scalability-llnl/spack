# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Setxkbmap(AutotoolsPackage, XorgPackage):
    """setxkbmap is an X11 client to change the keymaps in the X server for a
    specified keyboard to use the layout determined by the options listed
    on the command line."""

    homepage = "https://cgit.freedesktop.org/xorg/app/setxkbmap"
    xorg_mirror_path = "app/setxkbmap-1.3.1.tar.gz"

    license("MIT")

    version("1.3.4", sha256="cc4113eab3cd70c28c986174aa30e62690e789723c874acc53e8d1f058d11f92")
    version("1.3.3", sha256="51ba28edf93a464a7444b53b154fd5e93dedd1e9bbcc85b636f4cf56986c4842")
    version("1.3.2", sha256="7e934afc55f161406f7dd99b5be8837e5d1478d8263776697b159d48461a1d3c")
    version("1.3.1", sha256="e24a73669007fa3b280eba4bdc7f75715aeb2e394bf2d63f5cc872502ddde264")

    depends_on("c", type="build")  # generated

    depends_on("libxkbfile")
    depends_on("libx11")
    depends_on("libxrandr", when="@1.3.3:")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
