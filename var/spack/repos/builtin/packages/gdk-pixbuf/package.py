# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GdkPixbuf(MesonPackage):
    """The Gdk Pixbuf is a toolkit for image loading and pixel buffer manipulation. It is used by
    GTK+ 2 and GTK+ 3 to load and manipulate images. In the past it was distributed as part of
    GTK+ 2 but it was split off into a separate package in preparation for the change to GTK+ 3."""

    homepage = "https://gitlab.gnome.org/GNOME/gdk-pixbuf"
    url = "https://ftp.acc.umu.se/pub/gnome/sources/gdk-pixbuf/2.40/gdk-pixbuf-2.40.0.tar.xz"
    git = "https://gitlab.gnome.org/GNOME/gdk-pixbuf"
    list_url = "https://ftp.acc.umu.se/pub/gnome/sources/gdk-pixbuf/"
    list_depth = 1

    license("LGPL-2.1-or-later", checked_by="wdconinc")

    version("2.42.12", sha256="b9505b3445b9a7e48ced34760c3bcb73e966df3ac94c95a148cb669ab748e3c7")
    # https://nvd.nist.gov/vuln/detail/CVE-2022-48622
    version(
        "2.42.10",
        sha256="ee9b6c75d13ba096907a2e3c6b27b61bcd17f5c7ebeab5a5b439d2f2e39fe44b",
        deprecated=True,
    )
    version(
        "2.42.9",
        sha256="28f7958e7bf29a32d4e963556d241d0a41a6786582ff6a5ad11665e0347fc962",
        deprecated=True,
    )
    version(
        "2.42.6",
        sha256="c4a6b75b7ed8f58ca48da830b9fa00ed96d668d3ab4b1f723dcf902f78bde77f",
        deprecated=True,
    )
    version(
        "2.42.2",
        sha256="83c66a1cfd591d7680c144d2922c5955d38b4db336d7cd3ee109f7bcf9afef15",
        deprecated=True,
    )

    depends_on("c", type="build")

    variant("tiff", default=False, description="Enable TIFF support(partially broken)")
    # Man page creation was getting docbook errors, see issue #18853
    variant("man", default=False, description="Enable man page creation")

    with default_args(type="build"):
        depends_on("meson@0.55.3:")
        depends_on("pkgconfig")
        depends_on("libxslt", when="+man")
        depends_on("docbook-xsl@1.79.2:", when="+man")

    depends_on("shared-mime-info", when="platform=linux")
    depends_on("gettext")
    depends_on("glib@2.38.0:")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("libtiff", when="+tiff")
    depends_on("gobject-introspection")

    # Replace the docbook stylesheet URL with the one that our docbook-xsl package uses/recognizes.
    patch("docbook-cdn.patch", when="+man")

    def url_for_version(self, version):
        url = "https://ftp.acc.umu.se/pub/gnome/sources/gdk-pixbuf/{0}/gdk-pixbuf-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def meson_args(self):
        args = [f"-Dman={'true' if self.spec.satisfies('+man') else 'false'}"]
        if self.spec.satisfies("@2.42.9:"):
            args.append(f"-Dtests={'true' if self.run_tests else 'false'}")
        return args

    def setup_build_environment(self, env):
        # The "post-install.sh" script uses gdk-pixbuf-query-loaders,
        # which was installed earlier.
        env.prepend_path("PATH", self.prefix.bin)
