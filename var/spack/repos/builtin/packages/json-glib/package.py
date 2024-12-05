# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JsonGlib(MesonPackage):
    """JSON-GLib is a library for reading and parsing JSON using GLib and
    GObject data types and API."""

    homepage = "https://developer.gnome.org/json-glib"
    url = "https://ftp.gnome.org/pub/gnome/sources/json-glib/1.2/json-glib-1.2.8.tar.xz"
    list_url = "https://ftp.gnome.org/pub/gnome/sources/json-glib/"
    list_depth = 1

    license("LGPL-2.1-or-later")

    version("1.6.6", sha256="96ec98be7a91f6dde33636720e3da2ff6ecbb90e76ccaa49497f31a6855a490e")
    version(
        "1.5.2",
        sha256="ad08438327b6106dc040c0581477bdf1cd3daaa5d285920cc768b8627f746666",
        deprecated=True,
    )
    version(
        "1.4.4",
        sha256="720c5f4379513dc11fd97dc75336eb0c0d3338c53128044d9fabec4374f4bc47",
        deprecated=True,
    )
    version(
        "1.3.2",
        sha256="f6a80f42e63a3267356f20408bf91a1696837aa66d864ac7de2564ecbd332a7c",
        deprecated=True,
    )
    version(
        "1.2.8",
        sha256="fd55a9037d39e7a10f0db64309f5f0265fa32ec962bf85066087b83a2807f40a",
        deprecated=True,
    )

    depends_on("glib")
    depends_on("gobject-introspection")
    depends_on("pkgconfig", type="build")

    @when("@:1.5")
    def meson(self, spec, prefix):
        """Run the AutotoolsPackage configure phase"""
        configure("--prefix=" + prefix)

    @when("@:1.5")
    def build(self, spec, prefix):
        """Run the AutotoolsPackage build phase"""
        make()

    @when("@:1.5")
    def install(self, spec, prefix):
        """Run the AutotoolsPackage install phase"""
        make("install")
