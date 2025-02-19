# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxau(AutotoolsPackage, MesonPackage, XorgPackage):
    """The libXau package contains a library implementing the X11
    Authorization Protocol. This is useful for restricting client
    access to the display."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXau/"
    xorg_mirror_path = "lib/libXau-1.0.8.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    build_system("autotools", conditional("meson", when="@1.0.12:"), default="autotools")

    version("1.0.12", sha256="2402dd938da4d0a332349ab3d3586606175e19cb32cb9fe013c19f1dc922dcee")
    version("1.0.11", sha256="3a321aaceb803577a4776a5efe78836eb095a9e44bbc7a465d29463e1a14f189")
    version("1.0.10", sha256="51a54da42475d4572a0b59979ec107c27dacf6c687c2b7b04e5cf989a7c7e60c")
    version("1.0.9", sha256="1f123d8304b082ad63a9e89376400a3b1d4c29e67e3ea07b3f659cccca690eea")
    version("1.0.8", sha256="c343b4ef66d66a6b3e0e27aa46b37ad5cab0f11a5c565eafb4a1c7590bc71d7b")

    depends_on("c", type="build")

    depends_on("xproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXau", self.prefix, shared=True, recursive=True)
