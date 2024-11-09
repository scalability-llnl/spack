# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmodmap(AutotoolsPackage, XorgPackage):
    """The xmodmap program is used to edit and display the keyboard modifier
    map and keymap table that are used by client applications to convert
    event keycodes into keysyms.  It is usually run from the user's
    session startup script to configure the keyboard according to personal
    tastes."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xmodmap"
    xorg_mirror_path = "app/xmodmap-1.0.9.tar.gz"

    license("MIT")

    version("1.0.11", sha256="c4fac9df448b98ac5a1620f364e74ed5f7084baae0d09123700f34d4b63cb5d8")
    version("1.0.10", sha256="d4e9dc4cb034d0d774d059498d05348869934c52b0f24b0f3913823090b88640")
    version("1.0.9", sha256="73427a996f0fcda2a2c7ac96cfc4edd5985aeb13b48053f55ae7f63a668fadef")

    depends_on("c", type="build")

    depends_on("libx11")

    depends_on("xproto@7.0.25:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
