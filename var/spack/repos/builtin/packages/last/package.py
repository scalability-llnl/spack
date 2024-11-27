# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Last(MakefilePackage):
    """LAST finds similar regions between sequences, and aligns them. It is
    designed for comparing large datasets to each other (e.g. vertebrate
    genomes and/or large numbers of DNA reads)."""

    homepage = "http://last.cbrc.jp/"
    url = "http://last.cbrc.jp/last-869.zip"
    git = "https://gitlab.com/mcfrith/last.git"
    maintainers("snehring")

    license("GPL-3.0-only")

    version("1499", commit="2cc68d3ba8ae5ca46ceeb69302aef18b9db04f46")
    version("1282", commit="4368be912f4759e52b549940276f1adf087f489a")
    version("869", sha256="6371a6282bc1bb02a5e5013cc463625f2ce3e7746ff2ea0bdf9fe6b15605a67c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    def edit(self, spec, prefix):
        if not spec.satisfies("target=x86_64:"):
            filter_file("-msse4", "", "makefile")
        files = ["mat-doc.sh", "mat-inc.sh", "seed-doc.sh", "seed-inc.sh"]
        if spec.satisfies("@1282:"):
            files.append("gc-inc.sh")
        with working_dir("build"):
            for f in files:
                set_executable(f)

    def install(self, spec, prefix):
        make("install", "prefix=%s" % prefix)
