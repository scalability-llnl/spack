# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxp(AutotoolsPackage, XorgPackage):
    """libXp - X Print Client Library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXp"
    xorg_mirror_path = "lib/libXp-1.0.3.tar.gz"

    maintainers("wdconinc")

    version("1.0.4", sha256="05e46af1ccb68f1752cca5879774a4fb9bf3b19fe088eb745034956e0c6fadba")
    version("1.0.3", sha256="f6b8cc4ef05d3eafc9ef5fc72819dd412024b4ed60197c0d5914758125817e9c")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    depends_on("libxext")
    depends_on("libxau")

    depends_on("xextproto", type="build")
    depends_on("printproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
