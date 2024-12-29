# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Thunar(AutotoolsPackage):
    """Thunar File Manager"""

    homepage = "https://docs.xfce.org/xfce/thunar/start"
    url = "https://archive.xfce.org/xfce/4.16/src/thunar-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")
    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="d1f4b080c97b9e390eff199aaaac7562fb20f031686f8d5ee5207e953bfc2feb")
    version("4.16.0", sha256="6277c448116a91ebfa564972645d8d79ef69864992a02bb164b7b13f98fdfd9b")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("notifications", default=True, description="Build with startup-notification support")
    variant("jpeg", default=True, description="Build with libjpeg support")
    variant("exif", default=True, description="Build with libexif support")
    variant("gdbus", default=True, description="Build with gdbus support")
    variant("gio-unix", default=True, description="Build with gio-unix support")
    variant("libnotify", default=True, description="Build with libnotify support")
    variant("freetype", default=True, description="Build with freetype support")

    extendable = True

    # Base requirements
    depends_on("intltool@0.39.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("exo")
        depends_on("libpng")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("libexif", when="+exif")
        depends_on("dbus-glib", when="+gdbus")
        depends_on("libnotify", when="+libnotify")
        depends_on("libjpeg", when="+jpeg")
        depends_on("freetype", when="+freetype")
        depends_on("startup-notification", when="+notifications")
        with when("+introspection"):
            depends_on("libxfce4util+introspection")
            depends_on("libxfce4ui+introspection")
            depends_on("gobject-introspection")
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
            depends_on("gobject-introspection@1.66:", when="+introspection")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@4.18"):
            # Fails to check in xcfe4 include subdirectory for the libxfce4kbd-private-3 tree
            env.append_flags("CPPFLAGS", f"-I{self.spec['libxfce4ui'].home.include.xfce4}")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("notifications")
        args += self.enable_or_disable("exif")
        args += self.enable_or_disable("gio-unix")
        args += ["--with-custom-thunarx-dirs-enabled"]
        return args
