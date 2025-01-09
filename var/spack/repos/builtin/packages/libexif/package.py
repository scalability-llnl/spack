# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libexif(AutotoolsPackage, SourceforgePackage):
    """A library to parse an EXIF file and read the data from those tags"""

    homepage = "https://libexif.github.io/"
    url = "https://github.com/libexif/libexif/releases/download/v0.6.24/libexif-0.6.24.tar.bz2"

    maintainers("TheQueasle")

    license("LGPL-2.1-or-later", checked_by="wdconinc")

    version("0.6.24", sha256="d47564c433b733d83b6704c70477e0a4067811d184ec565258ac563d8223f6ae")
    version("0.6.21", sha256="16cdaeb62eb3e6dfab2435f7d7bccd2f37438d21c5218ec4e58efa9157d4d41a")

    depends_on("c", type="build")
    depends_on("glib")

    def url_for_version(self, version):
        if self.spec.satisfies("@:0.6.21"):
            return f"https://downloads.sourceforge.net/project/libexif/libexif/{version}/libexif-{version}.tar.bz2"
        else:
            return f"https://github.com/libexif/libexif/releases/download/v{version}/libexif-{version}.tar.bz2"
