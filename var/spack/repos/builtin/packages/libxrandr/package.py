# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxrandr(AutotoolsPackage, XorgPackage):
    """libXrandr - X Resize, Rotate and Reflection extension library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXrandr"
    xorg_mirror_path = "lib/libXrandr-1.5.0.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.5.4", sha256="c72c94dc3373512ceb67f578952c5d10915b38cc9ebb0fd176a49857b8048e22")
    version("1.5.3", sha256="3ad316c1781fe2fe22574b819e81f0eff087a8560377f521ba932238b41b251f")
    version("1.5.0", sha256="1b594a149e6b124aab7149446f2fd886461e2935eca8dca43fe83a70cf8ec451")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    depends_on("libxext")
    depends_on("libxrender")

    depends_on("randrproto@1.5:", type=("build", "link"))
    depends_on("xextproto", type="build")
    depends_on("renderproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXrandr", self.prefix, shared=True, recursive=True)
