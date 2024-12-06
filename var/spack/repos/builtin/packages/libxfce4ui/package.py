# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfce4ui(AutotoolsPackage):
    """Widget sharing library for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/libxfce4ui/start"
    url = "https://archive.xfce.org/xfce/4.16/src/libxfce4ui-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="532247c4387c17bb9ef94a73147039b8d013c3131c95cdbd2fa85fbcc848d06b")
    version("4.16.0", sha256="8b06c9e94f4be88a9d87c47592411b6cbc32073e7af9cbd64c7b2924ec90ceaa")

    variant("glibtop", default=True, description="Build with glibtop support")
    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("vala", default=True, description="Build with vala support")
    variant("notification", default=True, description="Build with startup-notification support")

    depends_on("intltool@0.35.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("xfconf")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("libgtop@2", when="+glibtop")
        depends_on("startup-notification", when="+notification")
        with when("+introspection"):
            depends_on("gobject-introspection")
            depends_on("libxfce4util+introspection")
        with when("+vala"):
            depends_on("vala")
            depends_on("libxfce4util+vala")
        with when("@4.18:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
            depends_on("gobject-introspection@1.66:", when="+introspection")
        with when("@4.16:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("glibtop")
        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("vala")
        args += self.enable_or_disable("notification")

        return args

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
