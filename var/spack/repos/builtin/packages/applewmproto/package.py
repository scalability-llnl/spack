# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Applewmproto(AutotoolsPackage, XorgPackage):
    """Apple Rootless Window Management Extension.

    This extension defines a protcol that allows X window managers
    to better interact with the Mac OS X Aqua user interface when
    running X11 in a rootless mode."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/applewmproto"
    xorg_mirror_path = "proto/applewmproto-1.4.2.tar.gz"

    license("MIT")

    version("1.4.2", sha256="ff8ac07d263a23357af2d6ff0cca3c1d56b043ddf7797a5a92ec624f4704df2e")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
