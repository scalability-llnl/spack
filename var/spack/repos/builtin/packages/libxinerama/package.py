# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxinerama(AutotoolsPackage, XorgPackage):
    """libXinerama - API for Xinerama extension to X11 Protocol."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXinerama"
    xorg_mirror_path = "lib/libXinerama-1.1.3.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.5", sha256="2efa855cb42dc620eff3b77700d8655695e09aaa318f791f201fa60afa72b95c")
    version("1.1.4", sha256="64de45e18cc76b8e703cb09b3c9d28bd16e3d05d5cd99f2d630de2d62c3acc18")
    version("1.1.3", sha256="0ba243222ae5aba4c6a3d7a394c32c8b69220a6872dbb00b7abae8753aca9a44")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xextproto", type="build")
    depends_on("xineramaproto@1.1.99.1:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXinerama", self.prefix, shared=True, recursive=True)
