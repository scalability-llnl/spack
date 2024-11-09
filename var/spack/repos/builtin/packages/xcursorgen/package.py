# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcursorgen(AutotoolsPackage, XorgPackage):
    """xcursorgen prepares X11 cursor sets for use with libXcursor."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xcursorgen"
    xorg_mirror_path = "app/xcursorgen-1.0.6.tar.gz"

    version("1.0.8", sha256="b8bb2756918343b8bc15a4ce875e9efb6c4e7777adba088280e53dd09753b6ac")
    version("1.0.7", sha256="6bc32d4977ffd60c00583bfd217f1d1245ca54dafbfbbcdbf14f696f9487b83e")
    version("1.0.6", sha256="4559f2b6eaa93de4cb6968679cf40e39bcbe969b62ebf3ff84f6780f8048ef8c")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxcursor")
    depends_on("libpng@1.2.0:")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
