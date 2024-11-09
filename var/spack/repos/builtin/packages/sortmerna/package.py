# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sortmerna(CMakePackage):
    """SortMeRNA is a program tool for filtering, mapping and OTU-picking NGS
    reads in metatranscriptomic and metagenomic data"""

    homepage = "https://github.com/biocore/sortmerna"
    git = "https://github.com/biocore/sortmerna.git"

    license("LGPL-3.0-or-later")

    version("2017-07-13", commit="8bde6fa113a5d99a23ae81b48eeea6760e966094")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("sse2neon", when="target=aarch64:")

    patch("for_aarch64.patch", when="target=aarch64:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(join_path(self.build_directory, "src", "indexdb")):
            install("indexdb", prefix.bin)
        with working_dir(join_path(self.build_directory, "src", "sortmerna")):
            install("sortmerna", prefix.bin)
