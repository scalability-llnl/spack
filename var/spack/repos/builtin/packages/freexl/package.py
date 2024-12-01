# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freexl(AutotoolsPackage):
    """FreeXL is an open source library to extract valid data from within
    an Excel (.xls) spreadsheet."""

    homepage = "https://www.gaia-gis.it"
    url = "http://www.gaia-gis.it/gaia-sins/freexl-1.0.5.tar.gz"

    version("2.0.0", sha256="176705f1de58ab7c1eebbf5c6de46ab76fcd8b856508dbd28f5648f7c6e1a7f0")
    version("1.0.6", sha256="3de8b57a3d130cb2881ea52d3aa9ce1feedb1b57b7daa4eb37f751404f90fc22")
    version("1.0.5", sha256="3dc9b150d218b0e280a3d6a41d93c1e45f4d7155829d75f1e5bf3e0b0de6750d")

    depends_on("c", type="build")

    depends_on("minizip", when="@2:")
    depends_on("expat", type="link")
    depends_on("iconv", type="link")

    def flag_handler(self, name, flags):
        # avoid that header is taken from libiconv, but library from libc -- configure script is
        # missing a compile + link test.
        iconv = self.spec["iconv"]
        if name == "ldflags" and iconv.name == "libiconv":
            flags.append(iconv.libs.ld_flags)
        return (flags, None, None)
