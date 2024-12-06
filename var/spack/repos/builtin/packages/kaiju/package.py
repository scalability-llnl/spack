# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kaiju(MakefilePackage):
    """Kaiju is a program for the taxonomic classification
    of high-throughput sequencing reads."""

    homepage = "https://github.com/bioinformatics-centre/kaiju"
    url = "https://github.com/bioinformatics-centre/kaiju/archive/v1.6.2.zip"

    license("GPL-3.0-or-later")

    version("1.6.2", sha256="2685fed7e27ddeb26530fd60a4b388f2d5f3e29aaa79f8e2e6abcbac64075db8")

    build_directory = "src"

    depends_on("perl-io-compress", type="run")
    depends_on("py-htseq", type="run")

    def edit(self, spec, prefix):
        # Replace ftp:// with https://
        makedb = FileFilter("util/makeDB.sh")
        makedb.filter("ftp://", "https://", string=True)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
