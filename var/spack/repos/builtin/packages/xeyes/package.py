# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xeyes(AutotoolsPackage, XorgPackage):
    """xeyes - a follow the mouse X demo, using the X SHAPE extension"""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xeyes"
    xorg_mirror_path = "app/xeyes-1.1.1.tar.gz"

    license("MIT")

    version("1.2.0", sha256="727e651fd4597f6aa131b67474372a081dccd28ea2cdd364f21dae6e59003ee8")
    version("1.1.2", sha256="4a675b34854da362bd8dff4f21ff92e0c19798b128ea0af24b7fc7c5ac2feea3")
    version("1.1.1", sha256="3a1871a560ab87c72a2e2ecb7fd582474448faec3e254c9bd8bead428ab1bca3")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")
    depends_on("libxmu")
    depends_on("libxrender@0.4:")
    depends_on("libxi@1.7:", when="@1.2:")
    depends_on("libxcb@1.9:", when="@1.2:")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
