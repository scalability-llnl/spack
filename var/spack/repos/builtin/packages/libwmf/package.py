# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libwmf(AutotoolsPackage):
    """libwmf is a library for reading vector images in Microsft's
    native Windows Metafile Format (WMF)"""

    homepage = "https://github.com/caolanm/libwmf"
    url = "https://github.com/caolanm/libwmf/archive/refs/tags/v0.2.12.tar.gz"

    maintainers("benkirk")

    parallel = False

    license("LGPL-2.0-or-later")

    version("0.2.13", sha256="18ba69febd2f515d98a2352de284a8051896062ac9728d2ead07bc39ea75a068")
    version("0.2.12", sha256="464ff63605d7eaf61a4a12dbd420f7a41a4d854675d8caf37729f5bc744820e2")
    version("0.2.11", sha256="e2a2664afd5abc71a42be7ad3c200f64de2b8889bf088eac1d32e205ce843803")

    patch(
        "https://github.com/caolanm/libwmf/commit/1f87c35bc2a36fdca760a4577761d30d9cc876e2.patch?full_index=1",
        sha256="80ae84a904baa21e1566e3d2bca1c6aaa0a2a30f684fe50f25e7e5751ef3ec93",
        when="@:0.2.13",
    )

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("expat")
    depends_on("freetype")
    depends_on("gdk-pixbuf")
    depends_on("ghostscript-fonts")
    depends_on("libxml2")
    depends_on("libpng")
    depends_on("libjpeg")
    depends_on("zlib-api")

    def configure_args(self):
        args = ["--disable-static"]
        return args
