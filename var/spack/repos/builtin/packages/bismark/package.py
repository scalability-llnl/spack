# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bismark(Package):
    """A tool to map bisulfite converted sequence reads and determine cytosine
    methylation states"""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/bismark"
    url = "https://github.com/FelixKrueger/Bismark/archive/0.23.0.tar.gz"

    license("GPL-3.0-only")

    version("0.24.1", sha256="c5409f5fa470ea5ac07327ced28c60b793f5ef88c5a7bc75b71dde0f52f39894")
    version("0.23.0", sha256="ea1625808487c1442dbf825d9cbe5c0cbc37ea5bd1460f59e1e0ccc80cc01c9e")
    version("0.19.0", sha256="91707737f96a0574956a282b635abad7560e7d90bee188a67a7807b2470deae2")
    version("0.18.2", sha256="83391c5b5af33047178e7774ac25f5a69ce9315c13ae02f016baf7c50b73e702")

    depends_on("bowtie2", type="run")
    depends_on("perl", type="run")
    depends_on("samtools", type="run")
    depends_on("hisat2", type="run", when="@0.21.0:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bam2nuc", prefix.bin)
        install("bismark", prefix.bin)
        install("bismark_genome_preparation", prefix.bin)
        install("bismark_methylation_extractor", prefix.bin)
        install("bismark2bedGraph", prefix.bin)
        install("bismark2report", prefix.bin)
        install("bismark2summary", prefix.bin)
        install("coverage2cytosine", prefix.bin)
        install("deduplicate_bismark", prefix.bin)
        install("filter_non_conversion", prefix.bin)
        install("NOMe_filtering", prefix.bin)
