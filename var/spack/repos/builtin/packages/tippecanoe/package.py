# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tippecanoe(MakefilePackage):
    """Build vector tilesets from large collections of GeoJSON features."""

    homepage = "https://github.com/mapbox/tippecanoe"
    url = "https://github.com/mapbox/tippecanoe/archive/1.34.3.tar.gz"

    license("BSD-2-Clause")

    version("1.36.0", sha256="0e385d1244a0d836019f64039ea6a34463c3c2f49af35d02c3bf241aec41e71b")
    version("1.34.3", sha256="7a2dd2376a93d66a82c8253a46dbfcab3eaaaaca7bf503388167b9ee251bee54")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("sqlite")
    depends_on("zlib-api")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"PREFIX \?= /usr/local", "PREFIX = " + self.prefix)
