# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfontcache(AutotoolsPackage, XorgPackage):
    """Xfontcache - X-TrueType font cache extension client library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXfontcache"
    xorg_mirror_path = "lib/libXfontcache-1.0.5.tar.gz"

    license("BSD-2-Clause")

    version("1.0.5", sha256="fdba75307a0983d2566554e0e9effa7079551f1b7b46e8de642d067998619659")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xextproto", type="build")
    depends_on("fontcacheproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
