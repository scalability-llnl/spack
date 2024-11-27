# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xset(AutotoolsPackage, XorgPackage):
    """User preference utility for X."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xset"
    xorg_mirror_path = "app/xset-1.2.3.tar.gz"

    license("MIT")

    version("1.2.5", sha256="2068d1356d80c29ce283f0fff5895667b38f24ea95df363d3dde7b8c8a92fffe")
    version("1.2.4", sha256="3a05e8626298c7a79002ec5fb4949dcba8abc7a2b95c03ed5e0f5698c3b4dea0")
    version("1.2.3", sha256="5ecb2bb2cbf3c9349b735080b155a08c97b314dacedfc558c7f5a611ee1297f7")

    depends_on("c", type="build")

    depends_on("libxmu")
    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
