# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxvmc(AutotoolsPackage, XorgPackage):
    """X.org libXvMC library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXvMC"
    xorg_mirror_path = "lib/libXvMC-1.0.9.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.0.14", sha256="3ad5d2b991219e2bf9b2f85d40b12c16f1afec038715e462f6058af73a9b5ef8")
    version("1.0.13", sha256="e630b4373af8c67a7c8f07ebe626a1269a613d262d1f737b57231a06f7c34b4e")
    version("1.0.12", sha256="024c9ec4f001f037eeca501ee724c7e51cf287eb69ced8c6126e16e7fa9864b5")
    version("1.0.11", sha256="0b931d216b23b95df87cc65f7bb7acef4120d9263adb0a4d90856ba1f7a390da")
    version("1.0.10", sha256="d8306f71c798d10409bb181b747c2644e1d60c05773c742c12304ab5aa5c8436")
    version("1.0.9", sha256="090f087fe65b30b3edfb996c79ff6cf299e473fb25e955fff1c4e9cb624da2c2")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    depends_on("libxext")
    depends_on("libxv")

    depends_on("xextproto", type=("build", "link"))
    depends_on("videoproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
