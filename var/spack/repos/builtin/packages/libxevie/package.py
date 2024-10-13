# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxevie(AutotoolsPackage, XorgPackage):
    """Xevie - X Event Interception Extension (XEvIE)."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXevie"
    xorg_mirror_path = "lib/libXevie-1.0.3.tar.gz"

    license("MIT")

    version("1.0.3", sha256="3759bb1f7fdade13ed99bfc05c0717bc42ce3f187e7da4eef80beddf5e461258")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xproto", type=("build", "link"))
    depends_on("xextproto", type="build")
    depends_on("evieext")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
