# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pharokka(Package):
    """pharokka is a rapid standardised annotation
    pipeline for bacteriophage genomes"""

    homepage = "https://github.com/gbouras13/pharokka"
    url = "https://github.com/gbouras13/pharokka/archive/refs/tags/v1.1.0.tar.gz"

    license("MIT")

    version("1.3.2", sha256="e12b20beada9c261f51dd37a9aa7afe83291363035dc53478c42fb67882900e1")
    version("1.1.0", sha256="57d546f501f201117f5d8037ac47c0d83ccd1ec518080145e8f28d3e9843fba6")

    depends_on("py-bcbio-gff", type="run")
    depends_on("py-biopython@1.78:", type="run")
    depends_on("py-phanotate@1.5.0:", type="run")
    depends_on("py-pandas", type="run")
    depends_on("mmseqs2@13.45111", type="run")
    depends_on("trnascan-se@2.0.9:", type="run")
    depends_on("prodigal@2.6.3:", type="run")
    depends_on("minced@0.4.2:", type="run")
    depends_on("aragorn@1.2.41:", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("bin", prefix.bin)
