# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fstobdf(AutotoolsPackage, XorgPackage):
    """The fstobdf program reads a font from a font server and prints a BDF
    file on the standard output that may be used to recreate the font.
    This is useful in testing servers, debugging font metrics, and
    reproducing lost BDF files."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/fstobdf"
    xorg_mirror_path = "app/fstobdf-1.0.6.tar.gz"

    version("1.0.7", sha256="5cf1f697415dc5f66df24d7495471dbd5bc3812580773e4c700ead5db27503cf")
    version("1.0.6", sha256="bb903ae76cbcb0a08a71f06762b64db7d5c2064f6e88e8dc3a604e76d0bcb93d")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libfs")

    depends_on("xproto@7.0.25:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
