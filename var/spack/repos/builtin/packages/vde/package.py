# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vde(AutotoolsPackage):
    """Ethernet compliant virtual network"""

    homepage = "https://github.com/virtualsquare/vde-2"
    url = "https://github.com/virtualsquare/vde-2/archive/refs/tags/v2.3.3.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later", checked_by="trws")

    version("2.3.3", sha256="a7d2cc4c3d0c0ffe6aff7eb0029212f2b098313029126dcd12dc542723972379")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose")
