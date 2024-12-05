# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xgc(AutotoolsPackage, XorgPackage):
    """xgc is an X11 graphics demo that shows various features of the X11
    core protocol graphics primitives."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xgc"
    xorg_mirror_path = "app/xgc-1.0.5.tar.gz"

    version("1.0.6", sha256="8b5cfc547c04a2bd0807be700349522c0e717e34387019dd209eefa83cfa74f0")
    version("1.0.5", sha256="16645fb437699bad2360f36f54f42320e33fce5a0ab9a086f6e0965963205b02")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libxt")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
