# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfce4Panel(AutotoolsPackage):
    """Panel manager for Xfce4"""

    homepage = "https://docs.xfce.org/xfce/xfce4-panel/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfce4-panel-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2 OR LGPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="be80023fd546587831bab25ded15ae4c9e346289a75744b6ba4cf4ee53794710")
    version("4.16.0", sha256="5e979aeeb37d306d72858b1bc67448222ea7a68de01409055b846cd31f3cc53d")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("notification", default=True, description="Build with startup-notification support")

    patch("fix-libxfce4util-gir.patch", when="@4.16.0")  # Capitalization difference causes error

    # Base requirements
    depends_on("intltool@0.51.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4ui")
        depends_on("libxfce4util")
        depends_on("exo")
        depends_on("garcon")
        depends_on("libwnck@3:")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("startup-notification", when="+notification")
        with when("+introspection"):
            depends_on("libxfce4ui+introspection")
            depends_on("gobject-introspection")
            depends_on("gobject-introspection")
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
            depends_on("gobject-introspection@1.66:", when="+introspection")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        return args
