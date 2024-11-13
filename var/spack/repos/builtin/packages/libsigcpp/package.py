# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsigcpp(AutotoolsPackage):
    """Libsigc++ is a C++ library for typesafe callbacks"""

    homepage = "https://libsigcplusplus.github.io/libsigcplusplus/index.html"
    url = "https://ftp.acc.umu.se/pub/GNOME/sources/libsigc++/2.99/libsigc++-2.99.12.tar.xz"
    list_url = "https://ftp.acc.umu.se/pub/GNOME/sources/libsigc++/"
    list_depth = 1

    license("LGPL-3.0-only")

    version("2.99.12", sha256="d902ae277f5baf2d56025586e2153cc2f158472e382723c67f49049f7c6690a8")
    version("2.9.3", sha256="0bf9b301ad6198c550986c51150a646df198e8d1d235270c16486b0dda30097f")
    version("2.1.1", sha256="7a2bd0b521544b31051c476205a0e74ace53771ec1a939bfec3c297b50c9fd78")
    version("2.0.3", sha256="6ee6d5f164d8a34da33d2251cdb348b4f5769bf993ed8a6d4055bd47562f94a2")

    depends_on("cxx", type="build")  # generated

    depends_on("m4", when="@:2.9", type="build")

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/libsigc++"
        ext = ".tar.gz" if version < Version("2.2.10") else ".tar.xz"
        return url + "/%s/libsigc++-%s%s" % (version.up_to(2), version, ext)

    def configure_args(self):
        return ["--enable-static"]
