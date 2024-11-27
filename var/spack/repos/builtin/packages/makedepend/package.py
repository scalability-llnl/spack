# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Makedepend(AutotoolsPackage, XorgPackage):
    """makedepend - create dependencies in makefiles."""

    homepage = "https://gitlab.freedesktop.org/xorg/util/makedepend"
    xorg_mirror_path = "util/makedepend-1.0.5.tar.gz"

    license("MIT-open-group")

    version("1.0.9", sha256="bc94ffda6cd4671603a69c39dbe8f96b317707b9185b2aaa3b54b5d134b41884")
    version("1.0.8", sha256="275f0d2b196bfdc740aab9f02bb48cb7a97e4dfea011a7b468ed5648d0019e54")
    version("1.0.5", sha256="503903d41fb5badb73cb70d7b3740c8b30fe1cc68c504d3b6a85e6644c4e5004")

    depends_on("c", type="build")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
