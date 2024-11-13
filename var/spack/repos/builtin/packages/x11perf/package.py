# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class X11perf(AutotoolsPackage, XorgPackage):
    """Simple X server performance benchmarker."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/x11perf"
    xorg_mirror_path = "app/x11perf-1.6.0.tar.gz"

    version("1.6.1", sha256="a1874618df0e30ae1a9b2470fb50e77a40c4a6f6ddf87a5c154f7a3b913ac0b3")
    version("1.6.0", sha256="d33051c4e93100ab60609aee14ff889bb2460f28945063d793e21eda19381abb")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxmu")
    depends_on("libxrender")
    depends_on("libxft")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
