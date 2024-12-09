# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxext(AutotoolsPackage, XorgPackage):
    """libXext - library for common extensions to the X11 protocol."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXext"
    xorg_mirror_path = "lib/libXext-1.3.3.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.3.6", sha256="1a0ac5cd792a55d5d465ced8dbf403ed016c8e6d14380c0ea3646c4415496e3d")
    version("1.3.5", sha256="1a3dcda154f803be0285b46c9338515804b874b5ccc7a2b769ab7fd76f1035bd")
    version("1.3.4", sha256="8ef0789f282826661ff40a8eef22430378516ac580167da35cc948be9041aac1")
    version("1.3.3", sha256="eb0b88050491fef4716da4b06a4d92b4fc9e76f880d6310b2157df604342cfe5")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")

    depends_on("xproto@7.0.13:", type="build")
    depends_on("xextproto@7.2:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXext", self.prefix, shared=True, recursive=True)
