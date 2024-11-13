# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libcroco(AutotoolsPackage):
    """Libcroco is a standalone css2 parsing and manipulation library."""

    homepage = "https://developer.gnome.org/libcroco"
    url = "http://ftp.gnome.org/pub/gnome/sources/libcroco/0.6/libcroco-0.6.12.tar.xz"

    license("LGPL-2.0-or-later")

    version("0.6.13", sha256="767ec234ae7aa684695b3a735548224888132e063f92db585759b422570621d4")
    version("0.6.12", sha256="ddc4b5546c9fb4280a5017e2707fbd4839034ed1aba5b7d4372212f34f84f860")

    depends_on("c", type="build")  # generated

    variant("doc", default=False, description="Build documentation with gtk-doc")

    depends_on("glib")
    depends_on("libxml2")
    depends_on("gtk-doc", type="build", when="+doc")
    depends_on("docbook-xml", type="build", when="+doc")
    depends_on("docbook-xsl", type="build", when="+doc")
    depends_on("py-pygments", type="build", when="+doc")
    depends_on("pkgconfig", type="build")

    def configure_args(self):
        config_args = []
        if self.spec.satisfies("+doc"):
            config_args.extend(
                [
                    "--enable-gtk-doc",
                    "--enable-gtk-doc-html",
                    # PDF not supported in gtk-doc
                    "--disable-gtk-doc-pdf",
                ]
            )
        else:
            config_args.extend(
                ["--disable-gtk-doc", "--disable-gtk-doc-html", "--disable-gtk-doc-pdf"]
            )

        # macOS ld does not support this flag
        # https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/libcroco.rb
        if self.spec.satisfies("platform=darwin"):
            config_args.append("--disable-Bsymbolic")

        return config_args
