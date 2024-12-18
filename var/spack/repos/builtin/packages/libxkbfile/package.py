# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxkbfile(AutotoolsPackage, XorgPackage):
    """XKB file handling routines."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxkbfile"
    xorg_mirror_path = "lib/libxkbfile-1.0.9.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.3", sha256="c4c2687729d1f920f165ebb96557a1ead2ef655809ab5eaa66a1ad36dc31050d")
    version("1.1.2", sha256="d1a7e659bc7ae1aa1fc1ecced261c734df5ad5d86af1ef7a946be0e2d841e51d")
    version("1.1.1", sha256="87faee6d4873c5631e8bb53e85134084b862185da682de8617f08ca18d82e216")
    version("1.1.0", sha256="2a92adda3992aa7cbad758ef0b8dfeaedebb49338b772c64ddf369d78c1c51d3")
    version("1.0.9", sha256="95df50570f38e720fb79976f603761ae6eff761613eb56f258c3cb6bab4fd5e3")

    depends_on("c", type="build")

    depends_on("libx11")

    depends_on("kbproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
