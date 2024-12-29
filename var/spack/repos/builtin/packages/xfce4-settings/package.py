# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfce4Settings(AutotoolsPackage):
    """Daemon, manager, and editor to centralize the configuration management for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/xfce4-settings/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfce4-settings-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("4.18.0", sha256="ed3f75837cb33cd694610fc87cd569c4782b7ac4e099143a3dbe8fff1f1c6a9d")
    version("4.16.0", sha256="67a1404fc754c675c6431e22a8fe0e5d79644fdfadbfe25a4523d68e1442ddc2")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("libxcursor", default=True, description="Build with Xcursor support")
    variant("libnotify", default=True, description="Build with libnotify support")

    # Base requirements
    with default_args(type=("build", "link", "run")):
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("garcon")
        depends_on("exo")
        depends_on("dbus-glib")
        depends_on("libxi")
        depends_on("libxrandr")
        depends_on("libxcursor", when="+libxcursor")
        depends_on("libnotify", when="+libnotify")
        with when("+introspection"):
            depends_on("libxfce4util+introspection")
            depends_on("libxfce4ui+introspection")
            depends_on("gobject-introspection")

    depends_on("intltool@0.39.0:", type="build")
    with default_args(type=("build", "link", "run")):
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gobject-introspection@1.66:", when="+introspection")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("libxcursor")
        args += self.enable_or_disable("libnotify")
        args += self.enable_or_disable("introspection")
        return args
