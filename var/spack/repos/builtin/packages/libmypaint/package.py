# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmypaint(AutotoolsPackage):
    """libmypaint - MyPaint brush engine library.

    This is the brush library used by MyPaint. A number of other painting programs use it too."""

    homepage = "https://github.com/mypaint/libmypaint"
    url = "https://github.com/mypaint/libmypaint/releases/download/v1.6.1/libmypaint-1.6.1.tar.xz"

    maintainers("benkirk")

    license("ISC")

    version("1.6.1", sha256="741754f293f6b7668f941506da07cd7725629a793108bb31633fb6c3eae5315f")
    version("1.6.0", sha256="a5ec3624ba469b7b35fd66b6fbee7f07285b7a7813d02291ac9b10e46618140e")
    version("1.5.1", sha256="aef8150a0c84ce2ff6fb24de8d5ffc564845d006f8bad7ed84ee32ed1dd90c2b")
    version("1.4.0", sha256="59d13b14c6aca0497095f29ee7228ca2499a923ba8e1dd718a2f2ecb45a9cbff")
    version("1.3.0", sha256="6a07d9d57fea60f68d218a953ce91b168975a003db24de6ac01ad69dcc94a671")

    depends_on("c", type="build")
    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")

    variant("gegl", default=False, description="Enable GEGL based code in build")
    variant("introspection", default=True, description="Enable introspection for this build")

    depends_on("intltool")
    depends_on("json-c")
    depends_on("perl@5.8.1:")
    depends_on("perl-xml-parser")
    depends_on("babl", when="+gegl")
    depends_on("gegl", when="+gegl")
    depends_on("gobject-introspection", when="+introspection")
    depends_on("glib", when="+introspection")

    def configure_args(self):
        args = []

        if self.spec.satisfies("+gegl"):
            args.append("--enable-gegl=yes")

        if self.spec.satisfies("+introspection"):
            args.extend(
                ["--enable-introspection=yes", "--with-glib={0}".format(self.spec["glib"].prefix)]
            )

        return args
