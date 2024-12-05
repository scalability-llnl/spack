# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GsettingsDesktopSchemas(MesonPackage):
    """gsettings-desktop-schemas contains a collection of GSettings schemas
    for settings shared by various components of a desktop."""

    homepage = "https://github.com/GNOME/gsettings-desktop-schemas/"
    url = "https://github.com/GNOME/gsettings-desktop-schemas/archive/3.38.0.tar.gz"

    license("LGPL-2.0-or-later")

    version("3.38.0", sha256="b808bd285ac7176f2e9e3a8763c3913121ab9f109d2988c70e3f1f8e742a630d")
    version("3.37.92", sha256="5f5dd0421ed2f3746674b8bb6e0c652784915133c7f2d133339bf5e4140d8d1d")
    version("3.37.2", sha256="1dacdfeecfc57468da7c598a01b635f82ecd088e1d78d5aa840e47256026654d")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("gobject-introspection", type="build")
    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
