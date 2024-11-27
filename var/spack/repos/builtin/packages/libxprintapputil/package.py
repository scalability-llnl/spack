# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxprintapputil(AutotoolsPackage, XorgPackage):
    """Xprint application utility routines."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXprintAppUtil/"
    xorg_mirror_path = "lib/libXprintAppUtil-1.0.1.tar.gz"

    version("1.0.1", sha256="5af3939ffe15508b942bc1e325a29a95b1c85e8900a5f65a896101e63048bbf7")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxp")
    depends_on("libxprintutil")
    depends_on("libxau")

    depends_on("printproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
