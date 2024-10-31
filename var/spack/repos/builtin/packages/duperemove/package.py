# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Duperemove(MakefilePackage):
    """Duperemove is a simple tool for finding duplicated extents
    and submitting them for deduplication."""

    homepage = "https://github.com/markfasheh/duperemove"
    url = "https://github.com/markfasheh/duperemove/archive/v0.11.1.tar.gz"

    license("GPL-2.0-only")

    version("0.11.1", sha256="75c3c91baf7e5195acad62eab73a7afc3d0b88cbfccefac3e3412eba06a42ac8")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("sqlite")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("duperemove", prefix.bin)
