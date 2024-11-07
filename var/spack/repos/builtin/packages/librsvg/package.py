# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librsvg(AutotoolsPackage):
    """Library to render SVG files using Cairo"""

    homepage = "https://wiki.gnome.org/Projects/LibRsvg"
    url = "https://download.gnome.org/sources/librsvg/2.44/librsvg-2.44.14.tar.xz"

    license("LGPL-2.1-or-later")

    version("2.56.2", sha256="3ec3c4d8f73e0ba4b9130026969e8371c092b734298d36e2fdb3eb4afcec1200")
    version("2.51.0", sha256="89d32e38445025e1b1d9af3dd9d3aeb9f6fce527aeecbecf38b369b34c80c038")
    version("2.50.2", sha256="6211f271ce4cd44a7318190d36712e9cea384a933d3e3570004edeb210a056d3")
    version("2.50.0", sha256="b3fadba240f09b9c9898ab20cb7311467243e607cf8f928b7c5f842474ee3df4")
    version("2.44.17", sha256="91bea64669203c677d5efbe21175aabbadf36754c7e7a1d1dc016dff4425273b")
    version("2.44.14", sha256="6a85a7868639cdd4aa064245cc8e9d864dad8b8e9a4a8031bb09a4796bc4e303")
    version("2.40.21", sha256="f7628905f1cada84e87e2b14883ed57d8094dca3281d5bcb24ece4279e9a92ba")

    depends_on("c", type="build")  # generated

    variant("doc", default=False, description="Build documentation with gtk-doc")

    depends_on("gobject-introspection", type="build")
    depends_on("pkgconfig", type="build")
    # rust minimal version from NEWS file
    depends_on("rust@1.65:", when="@2.56.1:", type="build")
    # upper bound because "Unaligned references to packed fields are a hard
    # error" starting from 1.69
    depends_on("rust@1.40:1.68", when="@2.50:2.51", type="build")
    depends_on("rust", when="@2.41:", type="build")
    depends_on("gtk-doc", type="build", when="+doc")

    # requirements according to `configure` file
    depends_on("cairo@1.16:+gobject+png", when="@2.50:")
    depends_on("cairo@1.15.12:+gobject+png", when="@2.44.14:")
    depends_on("cairo@1.2.0:+gobject+png")
    depends_on("libcroco@0.6.1:", when="@:2.44.14")
    depends_on("gdk-pixbuf@2.20:")
    depends_on("glib@2.50:", when="@2.50:")
    depends_on("glib@2.48:", when="@2.44.14:")
    depends_on("glib@2.12:")
    depends_on("harfbuzz@2:", when="@2.50:")
    depends_on("libxml2@2.9:")
    depends_on("pango@1.46:", when="@2.51:")
    depends_on("pango@1.38:")

    depends_on("libffi")
    depends_on("shared-mime-info")
    depends_on("py-docutils", type="build")

    def url_for_version(self, version):
        url = "https://download.gnome.org/sources/librsvg/"
        url += "{0}/librsvg-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        # librsvg uses pthread_atfork() but does not use -pthread on Ubuntu 18.04 %gcc@8
        env.append_flags("LDFLAGS", "-pthread")

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def configure_args(self):
        args = []
        if self.spec.satisfies("+doc"):
            args.append("--enable-gtk-doc")
        else:
            args.extend(
                [
                    "--disable-gtk-doc",
                    "GTKDOC_MKPDF=/bin/true",
                    "GTKDOC_REBASE=/bin/true",
                    "GTKDOC_CHECK_PATH=/bin/true",
                ]
            )
        return args
