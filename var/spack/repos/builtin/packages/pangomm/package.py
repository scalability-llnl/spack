# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pangomm(AutotoolsPackage):
    """Pangomm is a C++ interface to Pango."""

    homepage = "https://www.pango.org/"
    url = "https://ftp.gnome.org/pub/GNOME/sources/pangomm/2.14/pangomm-2.14.1.tar.gz"

    license("LGPL-2.1-or-later AND GPL-2.0-or-later")

    version("2.43.1", sha256="00483967b4ed0869da09dc0617de45625b9ab846c7b07aa25dfc940a4fc540a4")
    version("2.42.0", sha256="ca6da067ff93a6445780c0b4b226eb84f484ab104b8391fb744a45cbc7edbf56")
    version("2.41.5", sha256="5131830d5b37b181ca4fa8f641ad86faa985c0bb7dcc833c98672d294367b304")
    version("2.40.2", sha256="0a97aa72513db9088ca3034af923484108746dba146e98ed76842cf858322d05")
    version("2.39.1", sha256="10c06bbf12a03963ffe9c697887b57c72f1dac1671d09dba45cecd25db5dc6ed")
    version("2.38.1", sha256="effb18505b36d81fc32989a39ead8b7858940d0533107336a30bc3eef096bc8b")
    version("2.37.2", sha256="bb83d769f4d4256e0b108e84a4f0441065da8483c7cc51518b0634668ed094f5")
    version("2.36.0", sha256="a8d96952c708d7726bed260d693cece554f8f00e48b97cccfbf4f5690b6821f0")
    version("2.35.1", sha256="3eb4d11014d09627b2b7c532c65b54fa182905b4c9688901ae11cdfb506dbc55")
    version("2.34.0", sha256="0e82bbff62f626692a00f3772d8b17169a1842b8cc54d5f2ddb1fec2cede9e41")
    version("2.28.4", sha256="778dcb66a793cbfd52a9f92ee5a71b888c3603a913fc1ddc48a30204de6d6c82")
    version("2.27.1", sha256="0d707b4a9e632223f7f27215f83fff679166cc89b9b7f209e7fe049af7b4562e")
    version("2.26.3", sha256="4f68e4d2d4b6c4ae82327ebd9e69f2cbc4379e502d12856c36943399b87d71a2")
    version("2.25.1", sha256="25684058138050a35ebb4f4e13899aea12045dfb00cc351dfe78f01cb1a1f21c")
    version("2.24.0", sha256="24c7b8782b8986fa8f6224ac1e5f1a02412b7d8bc21b53d14d6df9c7d9b59a3f")
    version("2.14.1", sha256="2ea6cee273cca1aae2ee5a5dac0c416b4dc354e46debb51f20c6eeba828f5ed5")
    version("2.14.0", sha256="baa3b231c9498fb1140254e3feb4eb93c638f07e6e26ae0e36c3699ec14d80fd")

    depends_on("cxx", type="build")  # generated

    depends_on("pango")
    depends_on("glibmm")
    depends_on("cairomm")

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/pangomm"
        ext = ".tar.gz" if version < Version("2.28.3") else ".tar.xz"
        return url + "/%s/pangomm-%s%s" % (version.up_to(2), version, ext)
