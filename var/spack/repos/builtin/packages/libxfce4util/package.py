# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libxfce4util(AutotoolsPackage):
    """Libxfce4util common  non-GTK+ utilities among the Xfce applications."""

    homepage = "https://docs.xfce.org/xfce/libxfce4util/start"
    url = "https://archive.xfce.org/xfce/4.16/src/libxfce4util-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teague")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="1157ca717fd3dd1da7724a6432a4fb24af9cd922f738e971fd1fd36dfaeac3c9")
    version("4.16.0", sha256="60598d745d1fc81ff5ad3cecc3a8d1b85990dd22023e7743f55abd87d8b55b83")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("vala", default=True, description="Build with vala support")

    with default_args(type="build"):
        depends_on("intltool@0.35.0:", when="@4.16:")
        depends_on("gettext", when="@4.18:")

    with default_args(type=("run", "link", "build")):
        depends_on("pkgconfig@0.9.0:")
        depends_on("glib@2")
        depends_on("gobject-introspection", when="+introspection")
        depends_on("vala", when="+vala")
        with when("@4.18:"):
            depends_on("glib@2.66:")
            depends_on("gobject-introspection@1.66:", when="+introspection")
        with when("@4.16"):
            depends_on("glib@2.50:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("vala")

        return args

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
