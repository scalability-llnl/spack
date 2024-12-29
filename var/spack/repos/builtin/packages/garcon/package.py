# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Garcon(AutotoolsPackage):
    """Menu library for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/garcon/start"
    url = "https://archive.xfce.org/xfce/4.16/src/garcon-0.8.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="54633487566a8b8502b71c11a7f719efe27c069bd5773cc95f11ff4ea8f11a14")
    version("0.8.0", sha256="4811d89ee5bc48dbdeffd69fc3eec6c112bbf01fde98a9e848335b374a4aa1bb")

    variant("introspection", default=True, description="Build with gobject-introspection support")

    # Base requirements
    depends_on("intltool@0.51.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
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

    def setup_dependent_build_environment(self, env, dep_spec):
        if self.spec.satisfies("+introspection") and dep_spec.satisfies("+introspection"):
            env.append_path("XDG_DATA_DIRS", self.prefix.share)
