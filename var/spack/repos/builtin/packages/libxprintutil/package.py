# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxprintutil(AutotoolsPackage, XorgPackage):
    """Xprint application utility routines."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXprintUtil/"
    xorg_mirror_path = "lib/libXprintUtil-1.0.1.tar.gz"

    version("1.0.1", sha256="220924216f98ef8f7aa4cff33629edb1171ad10f8ea302a1eb85055545d4d195")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxp")
    depends_on("libxt")
    depends_on("libxau")

    depends_on("printproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
