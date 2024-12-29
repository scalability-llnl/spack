# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxxf86vm(AutotoolsPackage, XorgPackage):
    """libXxf86vm - Extension library for the XFree86-VidMode X extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXxf86vm"
    xorg_mirror_path = "lib/libXxf86vm-1.1.4.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.5", sha256="f3f1c29fef8accb0adbd854900c03c6c42f1804f2bc1e4f3ad7b2e1f3b878128")
    version("1.1.4", sha256="5108553c378a25688dcb57dca383664c36e293d60b1505815f67980ba9318a99")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    depends_on("libxext")

    depends_on("xproto", type="build")
    depends_on("xextproto", type="build")
    depends_on("xf86vidmodeproto@2.2.99.1:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXxf86vm", self.prefix, shared=True, recursive=True)
