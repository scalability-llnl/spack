# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Atk(MesonPackage):
    """ATK provides the set of accessibility interfaces that are
    implemented by other toolkits and applications. Using the ATK
    interfaces, accessibility tools have full access to view and
    control running applications."""

    homepage = "https://developer.gnome.org/atk/"
    url = "https://ftp.gnome.org/pub/gnome/sources/atk/2.30/atk-2.30.0.tar.xz"
    list_url = "https://ftp.gnome.org/pub/gnome/sources/atk"
    list_depth = 1

    license("LGPL-2.0-or-later")

    version("2.38.0", sha256="ac4de2a4ef4bd5665052952fe169657e65e895c5057dffb3c2a810f6191a0c36")
    version("2.36.0", sha256="fb76247e369402be23f1f5c65d38a9639c1164d934e40f6a9cf3c9e96b652788")
    version("2.30.0", sha256="dd4d90d4217f2a0c1fee708a555596c2c19d26fef0952e1ead1938ab632c027b")
    version("2.28.1", sha256="cd3a1ea6ecc268a2497f0cd018e970860de24a6d42086919d6bf6c8e8d53f4fc")

    depends_on("c", type="build")

    depends_on("meson@0.40.1:", type="build")
    depends_on("meson@0.46.0:", type="build", when="@2.29:")
    depends_on("glib")
    depends_on("gettext")
    depends_on("pkgconfig", type="build")
    depends_on("gobject-introspection")
    depends_on("libffi")

    def url_for_version(self, version):
        return (
            f"http://ftp.gnome.org/pub/gnome/sources/atk/"
            f"{version.up_to(2)}/atk-{version}.tar.xz"
        )

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))
