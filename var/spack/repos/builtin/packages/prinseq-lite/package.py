# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PrinseqLite(Package):
    """PRINSEQ will help you to preprocess your genomic or metagenomic
    sequence data in FASTA or FASTQ format."""

    homepage = "https://prinseq.sourceforge.net"
    url = "https://sourceforge.net/projects/prinseq/files/standalone/prinseq-lite-0.20.4.tar.gz"

    license("GPL-3.0-only")

    version("0.20.4", sha256="9b5e0dce3b7f02f09e1cc7e8a2dd77c0b133e5e35529d570ee901f53ebfeb56f")

    variant("nopca", default=True, description="Graphs version without PCA")

    depends_on("perl", type="run")
    depends_on("perl-cairo", type="run")
    depends_on("perl-digest-md5", type="run")
    depends_on("perl-json", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "prinseq-graphs-noPCA.pl")

        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "prinseq-lite.pl")

        install("prinseq-graphs-noPCA.pl", prefix.bin)
        install("prinseq-lite.pl", prefix.bin)

        chmod = which("chmod")
        chmod("+x", join_path(self.prefix.bin, "prinseq-graphs-noPCA.pl"))
        chmod("+x", join_path(self.prefix.bin, "prinseq-lite.pl"))
