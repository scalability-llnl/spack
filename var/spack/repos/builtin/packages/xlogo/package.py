# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlogo(AutotoolsPackage, XorgPackage):
    """The xlogo program simply displays the X Window System logo."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xlogo"
    xorg_mirror_path = "app/xlogo-1.0.4.tar.gz"

    version("1.0.6", sha256="0b0dbd90f53103b9241cc3a68c232213cec5c1d9a839604e59d128e4d81d1a4d")
    version("1.0.5", sha256="28f51b64e3bce6aa5ac0e35d0c12121e6e0311d3bd8b48664a57a74f6be651eb")
    version("1.0.4", sha256="0072eb3b41af77d5edfafb12998c7dd875f2795dc94735a998fd2ed8fc246e57")

    depends_on("c", type="build")  # generated

    depends_on("libsm")
    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt@1.0:")
    depends_on("libxext")
    depends_on("libx11")
    depends_on("libxft")
    depends_on("libxrender")
    depends_on("libxt")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
