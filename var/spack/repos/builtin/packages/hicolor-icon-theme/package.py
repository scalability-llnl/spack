# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HicolorIconTheme(AutotoolsPackage):
    """icon-theme contains the standard also references the default
    icon theme called hicolor."""

    homepage = "https://www.freedesktop.org/wiki/Software/icon-theme/"
    url = "https://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.17.tar.xz"

    license("GPL-2.0-only")

    version("0.17", sha256="317484352271d18cbbcfac3868eab798d67fff1b8402e740baa6ff41d588a9d8")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
