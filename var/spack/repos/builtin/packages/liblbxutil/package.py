# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblbxutil(AutotoolsPackage, XorgPackage):
    """liblbxutil - Low Bandwith X extension (LBX) utility routines."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/liblbxutil"
    xorg_mirror_path = "lib/liblbxutil-1.1.0.tar.gz"

    license("libtiff")

    version("1.1.0", sha256="285c1bc688cc71ec089e9284f2566d1780cc5d90816e9997890af8689f386951")

    depends_on("c", type="build")

    depends_on("xextproto@7.0.99.1:", type="build")
    depends_on("xproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
    depends_on("zlib-api", type="link")

    # There is a bug in the library that causes the following messages:
    # undefined symbol: Xfree
    # undefined symbol: Xalloc
    # See https://bugs.freedesktop.org/show_bug.cgi?id=8421
    # Adding a dependency on libxdmcp and adding LIBS=-lXdmcp did not fix it
