# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prokka(Package):
    """Prokka is a software tool to annotate bacterial, archaeal and viral
    genomes quickly and produce standards-compliant output files."""

    homepage = "https://github.com/tseemann/prokka"
    url = "https://github.com/tseemann/prokka/archive/v1.14.5.tar.gz"

    version("1.14.6", sha256="f730b5400ea9e507bfe6c5f3d22ce61960a897195c11571c2e1308ce2533faf8")

    depends_on("perl", type="run")
    depends_on("perl-bioperl", type="run")
    depends_on("perl-xml-simple", type="run")
    depends_on("perl-bio-searchio-hmmer", type="run")
    depends_on("hmmer", type="run")
    depends_on("blast-plus", type="run")
    depends_on("prodigal", type="run")
    depends_on("tbl2asn", type="run")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("binaries", prefix.binaries)
        install_tree("db", prefix.db)
        install_tree("doc", prefix.doc)
