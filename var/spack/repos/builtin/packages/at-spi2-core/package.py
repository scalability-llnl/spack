# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AtSpi2Core(MesonPackage):
    """The At-Spi2 Core package provides a Service Provider Interface for the
    Assistive Technologies available on the GNOME platform and a library
    against which applications can be linked."""

    homepage = "https://www.linuxfromscratch.org/blfs/view/cvs/x/at-spi2-core.html"
    url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-core/2.28/at-spi2-core-2.38.0.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-core"
    list_depth = 1

    license("LGPL-2.1-or-later")

    version("2.54.0", sha256="d7eee7e75beddcc272cedc2b60535600f3aae6e481589ebc667afc437c0a6079")
    version("2.52.0", sha256="0ac3fc8320c8d01fa147c272ba7fa03806389c6b03d3c406d0823e30e35ff5ab")
    version("2.51.91", sha256="1344bd5c1732b55fcf3df9e3b87569f60984ae83ce75881b5a057c69f8d73e34")
    version("2.48.3", sha256="37316df43ca9989ce539d54cf429a768c28bb38a0b34950beadd0421827edf55")
    version("2.48.0", sha256="905a5b6f1790b68ee803bffa9f5fab4ceb591fb4fae0b2f8c612c54f1d4e8a30")
    version("2.47.90", sha256="71189c21af7bd084a12ab85b229c2d798936470b12fb0c3f177e37181fb6c00c")
    version("2.40.1", sha256="9f66e3a4ee42db897af478a826b1366d7011a6d55ddb7e9d4bfeb3300ab23856")
    version("2.38.0", sha256="84e36c3fe66862133f5fe229772b76aa2526e10de5014a3778f2fa46ce550da5")
    version("2.36.0", sha256="88da57de0a7e3c60bc341a974a80fdba091612db3547c410d6deab039ca5c05a")
    version("2.28.0", sha256="42a2487ab11ce43c288e73b2668ef8b1ab40a0e2b4f94e80fca04ad27b6f1c87")

    depends_on("c", type="build")  # generated

    depends_on("meson@0.46.0:", type="build")
    depends_on("glib@2.56.1:")
    depends_on("glib@2.68.1:", when="@2.51.91:")
    depends_on("dbus@1.12.8:")
    depends_on("dbus@1.12.20:", when="@2.51.91:")
    depends_on("gettext")
    depends_on("libx11")
    depends_on("libxi")
    depends_on("libxtst")
    depends_on("recordproto")
    depends_on("inputproto")
    depends_on("fixesproto")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")
    depends_on("gobject-introspection")
    depends_on("gobject-introspection@1.68.0:", when="@2.51.91:")

    @when("@2.40.1:")
    def patch(self):
        filter_file(r"dbus_broker.found\(\)", "false", "bus/meson.build")

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-core"
        return url + f"/{version.up_to(2)}/at-spi2-core-{version}.tar.xz"

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_build_environment(self, env):
        # this avoids an "import site" error in the build
        env.unset("PYTHONHOME")
