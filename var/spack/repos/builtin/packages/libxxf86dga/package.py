# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxxf86dga(AutotoolsPackage, XorgPackage):
    """libXxf86dga - Client library for the XFree86-DGA extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXxf86dga"
    xorg_mirror_path = "lib/libXxf86dga-1.1.4.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.6", sha256="87c7482b1e29b4eeb415815641c4f69c00545a8138e1b73ff1f361f7d9c22ac4")
    version("1.1.5", sha256="715e2bf5caf6276f0858eb4b11a1aef1a26beeb40dce2942387339da395bef69")
    version("1.1.4", sha256="e6361620a15ceba666901ca8423e8be0c6ed0271a7088742009160349173766b")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xproto", type="build")
    depends_on("xextproto", type="build")
    depends_on("xf86dgaproto@2.0.99.2:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
