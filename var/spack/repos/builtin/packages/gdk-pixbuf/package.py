# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GdkPixbuf(Package):
    """The Gdk Pixbuf is a toolkit for image loading and pixel buffer
    manipulation. It is used by GTK+ 2 and GTK+ 3 to load and
    manipulate images. In the past it was distributed as part of
    GTK+ 2 but it was split off into a separate package in
    preparation for the change to GTK+ 3."""

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
    # https://nvd.nist.gov/vuln/detail/CVE-2021-20240
    version(
        "2.40.0",
        sha256="1582595099537ca8ff3b99c6804350b4c058bb8ad67411bbaae024ee7cead4e6",
        deprecated=True,
    )
    version(
        "2.38.2",
        sha256="73fa651ec0d89d73dd3070b129ce2203a66171dfc0bd2caa3570a9c93d2d0781",
        deprecated=True,
    )
    version(
        "2.38.0",
        sha256="dd50973c7757bcde15de6bcd3a6d462a445efd552604ae6435a0532fbbadae47",
        deprecated=True,
    )
    version(
        "2.31.2",
        sha256="9e467ed09894c802499fb2399cd9a89ed21c81700ce8f27f970a833efb1e47aa",
        deprecated=True,
    )

    depends_on("c", type="build")

    variant("x11", default=False, description="Enable X11 support", when="@:2.41")
    variant("tiff", default=False, description="Enable TIFF support(partially broken)")
    # Man page creation was getting docbook errors, see issue #18853
    variant("man", default=False, description="Enable man page creation")

    depends_on("meson@0.55.3:", type="build", when="@2.42.2:")
    depends_on("meson@0.46.0:", type="build", when="@2.37.92:")
    depends_on("meson@0.45.0:", type="build", when="@2.37.0:")
    depends_on("ninja", type="build", when="@2.37.0:")
    depends_on("shared-mime-info", when="@2.36.8: platform=linux")
    depends_on("pkgconfig", type="build")
    # Building the man pages requires libxslt and the Docbook stylesheets
    depends_on("libxslt", type="build", when="+man")
    depends_on("docbook-xsl@1.79.2:", type="build", when="+man")
    depends_on("gettext")
    depends_on("glib@2.38.0:")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("libtiff", when="+tiff")
    depends_on("gobject-introspection")
    depends_on("libx11", when="+x11")

    # Replace the docbook stylesheet URL with the one that our
    # docbook-xsl package uses/recognizes.
    # Pach modifies meson build files, so it only applies to versions that
    # depend on meson.
    patch("docbook-cdn.patch", when="@2.37.0:+man")

    def url_for_version(self, version):
        url = "https://ftp.acc.umu.se/pub/gnome/sources/gdk-pixbuf/{0}/gdk-pixbuf-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def install(self, spec, prefix):
        with working_dir("spack-build", create=True):
            meson_args = std_meson_args + ["-Dman={0}".format("+man" in spec)]
            # Only build tests when requested
            if self.version >= Version("2.42.9"):
                meson_args += ["-Dtests={0}".format(self.run_tests)]
            # Based on suggestion by luigi-calori and the fixup shown by lee218llnl:
            # https://github.com/spack/spack/pull/27254#issuecomment-974464174
            if spec.satisfies("+x11"):
                if self.version >= Version("2.42"):
                    raise InstallError("+x11 is not valid for {0}".format(self.version))
                meson_args += ["-Dx11=true"]
            meson("..", *meson_args)
            ninja("-v")
            if self.run_tests:
                ninja("test")
            ninja("install")

    def configure_args(self):
        args = []
        # disable building of gtk-doc files following #9771
        args.append("--disable-gtk-doc-html")
        true = which("true")
        args.append("GTKDOC_CHECK={0}".format(true))
        args.append("GTKDOC_CHECK_PATH={0}".format(true))
        args.append("GTKDOC_MKPDF={0}".format(true))
        args.append("GTKDOC_REBASE={0}".format(true))
        return args

    @when("@:2.36")
    def install(self, spec, prefix):
        configure("--prefix={0}".format(prefix), *self.configure_args())
        make()
        if self.run_tests:
            make("check")
        make("install")
        if self.run_tests:
            make("installcheck")

    def setup_build_environment(self, env):
        # The "post-install.sh" script uses gdk-pixbuf-query-loaders,
        # which was installed earlier.
        env.prepend_path("PATH", self.prefix.bin)
