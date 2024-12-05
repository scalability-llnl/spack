# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cufflinks(Package):
    """Cufflinks assembles transcripts, estimates their abundances, and tests
    for differential expression and regulation in RNA-Seq samples."""

    homepage = "https://cole-trapnell-lab.github.io/cufflinks"
    url = "https://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-2.2.1.Linux_x86_64.tar.gz"

    license("BSL-1.0")

    version("2.2.1", sha256="39f812452cae26462e5d2671d38104d9e8ef30aaf9ab6dea8ca57f50f46448e4")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("cuffcompare", prefix.bin)
        install("cuffdiff", prefix.bin)
        install("cufflinks", prefix.bin)
        install("cuffmerge", prefix.bin)
        install("cuffnorm", prefix.bin)
        install("cuffquant", prefix.bin)
        install("gffread", prefix.bin)
        install("gtf_to_sam", prefix.bin)
