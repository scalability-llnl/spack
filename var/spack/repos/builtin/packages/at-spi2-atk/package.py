# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AtSpi2Atk(MesonPackage):
    """The At-Spi2 Atk package contains a library that bridges ATK to
    At-Spi2 D-Bus service."""

    homepage = "https://www.linuxfromscratch.org/blfs/view/cvs/x/at-spi2-atk.html"
    url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk/2.26/at-spi2-atk-2.26.1.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk"
    list_depth = 1

    license("LGPL-2.1-or-later")

    version("2.38.0", sha256="cfa008a5af822b36ae6287f18182c40c91dd699c55faa38605881ed175ca464f")
    version("2.34.2", sha256="901323cee0eef05c01ec4dee06c701aeeca81a314a7d60216fa363005e27f4f0")
    version("2.26.2", sha256="61891f0abae1689f6617a963105a3f1dcdab5970c4a36ded9c79a7a544b16a6e")
    version("2.26.1", sha256="b4f0c27b61dbffba7a5b5ba2ff88c8cee10ff8dac774fa5b79ce906853623b75")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("at-spi2-core@2.28.0:2.45.1")
    depends_on("atk@2.28.1:")

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-atk"
        return url + f"/{version.up_to(2)}/at-spi2-atk-{version}.tar.xz"
