# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xvidtune(AutotoolsPackage, XorgPackage):
    """xvidtune is a client interface to the X server video mode
    extension (XFree86-VidModeExtension)."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xvidtune"
    xorg_mirror_path = "app/xvidtune-1.0.3.tar.gz"

    license("MIT")

    version("1.0.4", sha256="e5982c9e6c5009f0061c187a9cc82368215bd004cfa464a3d738c90e1d258668")
    version("1.0.3", sha256="c0e158388d60e1ce054ce462958a46894604bd95e13093f3476ec6d9bbd786d4")

    depends_on("c", type="build")  # generated

    depends_on("libxxf86vm")
    depends_on("libxt")
    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
