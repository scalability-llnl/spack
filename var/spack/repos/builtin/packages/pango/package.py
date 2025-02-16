# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pango(MesonPackage):
    """Pango is a library for laying out and rendering of text, with
    an emphasis on internationalization. It can be used anywhere
    that text layout is needed, though most of the work on Pango so
    far has been done in the context of the GTK+ widget toolkit."""

    homepage = "https://www.pango.org"
    url = "http://ftp.gnome.org/pub/GNOME/sources/pango/1.40/pango-1.40.3.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/pango/"
    list_depth = 1

    license("LGPL-2.1-or-later")

    # Do not upgrade to v1.90.x. It is a development release in preparation for
    # v2.0 that will break API and ABI compatibility. For more information see
    # https://download.gnome.org/sources/pango/1.90/pango-1.90.0.news
    version("1.54.0", sha256="8a9eed75021ee734d7fc0fdf3a65c3bba51dfefe4ae51a9b414a60c70b2d1ed8")
    version("1.52.2", sha256="d0076afe01082814b853deec99f9349ece5f2ce83908b8e58ff736b41f78a96b")
    version("1.50.13", sha256="5cdcf6d761d26a3eb9412b6cb069b32bd1d9b07abf116321167d94c2189299fd")
    version("1.50.7", sha256="0477f369a3d4c695df7299a6989dc004756a7f4de27eecac405c6790b7e3ad33")
    version("1.49.4", sha256="1fda6c03161bd1eacfdc349244d26828c586d25bfc600b9cfe2494902fdf56cf")
    version("1.48.11", sha256="084fd0a74fad05b1b299d194a7366b6593063d370b40272a5d3a1888ceb9ac40")
    version("1.47.0", sha256="730db8652fc43188e03218c3374db9d152351f51fc7011b9acae6d0a6c92c367")
    version("1.46.2", sha256="d89fab5f26767261b493279b65cfb9eb0955cd44c07c5628d36094609fc51841")
    version("1.45.5", sha256="f61dd911de2d3318b43bbc56bd271637a46f9118a1ee4378928c06df8a1c1705")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2019-1010238
        version(
            "1.44.6", sha256="3e1e41ba838737e200611ff001e3b304c2ca4cdbba63d200a20db0b0ddc0f86c"
        )
        version(
            "1.42.4", sha256="1d2b74cd63e8bd41961f2f8d952355aa0f9be6002b52c8aa7699d9f5da597c9d"
        )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("X", default=False, description="Enable an X toolkit")

    depends_on("meson@0.48:", type="build", when="@1.43:")
    depends_on("meson@0.50:", type="build", when="@1.44.4:")
    depends_on("meson@0.54:", type="build", when="@1.48.0:")
    depends_on("meson@0.55.3:", type="build", when="@1.48.1:")
    depends_on("meson@0.60:", type="build", when="@1.50.13:")
    depends_on("meson@0.63:", type="build", when="@1.54:")
    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("harfbuzz")
    depends_on("harfbuzz+coretext", when="platform=darwin")
    depends_on("cairo+ft+fc")
    depends_on("cairo~X", when="~X")
    depends_on("cairo+X", when="+X")
    depends_on("libxft", when="+X")
    depends_on("glib")
    depends_on("gobject-introspection")
    depends_on("fontconfig")
    depends_on("freetype@2:")
    depends_on("libffi")

    depends_on("cairo@1.12.10:", when="@1.41:")
    depends_on("fontconfig@2.11.91:", when="@1.41:")
    depends_on("glib@2.33.12:", when="@1.41:")
    depends_on("harfbuzz@1.2.3:", when="@1.41:")
    depends_on("libxft@2.0.0:", when="@1.41: +X")

    depends_on("fribidi@0.19.7:", when="@1.42:")
    depends_on("harfbuzz@1.2.3:", when="@1.42:")

    depends_on("glib@2.38.0:", when="@1.43:")
    depends_on("harfbuzz@1.4.2:", when="@1.43:")

    depends_on("glib@2.59.2:", when="@1.44:")
    depends_on("harfbuzz@2.0.0:", when="@1.44:")

    depends_on("glib@2.62:", when="@1.45:")
    depends_on("harfbuzz@2.2.0:", when="@1.48")

    depends_on("fontconfig@2.13.0:", when="@1.49:")
    depends_on("fribidi@1.0.6:", when="@1.49:")
    depends_on("harfbuzz@2.6.0:", when="@1.49:")
    depends_on("json-glib@1.6.0:", when="@1.49:")
    depends_on("gmake", type="build")

    def url_for_version(self, version):
        url = "http://ftp.gnome.org/pub/GNOME/sources/pango/{0}/pango-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def meson_args(self):
        spec = self.spec
        args = []

        # xft is not a meson option, even when it is a configure option
        if spec.satisfies("@1.49: +X"):
            args.append("-Dxft=enabled")
        elif spec.satisfies("@1.49: -X"):
            args.append("-Dxft=disabled")

        # disable building of gtk-doc files following #9885 and #9771
        if spec.satisfies("@1.54:"):
            args.append("-Ddocumentation=false")
        elif spec.satisfies("@1.44:"):
            args.append("-Dgtk_doc=false")
        else:
            args.append("-Denable_docs=false")

        return args

    @when("@:1.42")
    def configure_args(self):
        args = []
        if self.spec.satisfies("+X"):
            args.append("--with-xft")
        else:
            args.append("--without-xft")

        # disable building of gtk-doc files following #9885 and #9771
        args.append("--disable-gtk-doc-html")
        true = which("true")
        args.append(f"GTKDOC_CHECK={true}")
        args.append(f"GTKDOC_CHECK_PATH={true}")
        args.append(f"GTKDOC_MKPDF={true}")
        args.append(f"GTKDOC_REBASE={true}")

        return args

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    @when("@:1.42")
    def meson(self, spec, prefix):
        """Run the AutotoolsPackage configure phase"""
        configure("--prefix=" + prefix, *self.configure_args())

    @when("@:1.42")
    def build(self, spec, prefix):
        """Run the AutotoolsPackage build phase"""
        make()

    @when("@:1.42")
    def install(self, spec, prefix):
        """Run the AutotoolsPackage install phase"""
        make("install", parallel=False)
