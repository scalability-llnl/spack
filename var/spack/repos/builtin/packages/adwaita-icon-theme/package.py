# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AdwaitaIconTheme(AutotoolsPackage):
    """Mostly private use system icons."""

    homepage = "https://gitlab.gnome.org/GNOME/adwaita-icon-theme"
    url = "https://ftp.gnome.org/pub/gnome/sources/adwaita-icon-theme/3.38/adwaita-icon-theme-3.38.0.tar.xz"

    license("LGPL-3.0-or-later OR CC-BY-SA-3.0")

    version("3.38.0", sha256="6683a1aaf2430ccd9ea638dd4bfe1002bc92b412050c3dba20e480f979faaf97")

    depends_on("gdk-pixbuf", type="build")
    depends_on("librsvg", type="build")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
