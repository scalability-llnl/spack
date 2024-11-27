# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcursor(AutotoolsPackage, XorgPackage):
    """libXcursor - X Window System Cursor management library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXcursor"
    xorg_mirror_path = "lib/libXcursor-1.1.14.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.2.2", sha256="98c3a30a3f85274c167d1ac5419d681ce41f14e27bfa5fe3003c8172cd8af104")
    version("1.2.1", sha256="77f96b9ad0a3c422cfa826afabaf1e02b9bfbfc8908c5fa1a45094faad074b98")
    version("1.1.14", sha256="be0954faf274969ffa6d95b9606b9c0cfee28c13b6fc014f15606a0c8b05c17b")

    depends_on("c", type="build")

    depends_on("libxrender@0.8.2:")
    depends_on("libxfixes")
    depends_on("libx11")

    depends_on("fixesproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
