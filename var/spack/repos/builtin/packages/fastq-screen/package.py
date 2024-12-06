# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FastqScreen(Package):
    """FastQ Screen allows you to screen a library of sequences in FastQ format
    against a set of sequence databases so you can see if the composition of
    the library matches with what you expect."""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/"
    url = "https://github.com/StevenWingett/FastQ-Screen/archive/refs/tags/v0.15.3.tar.gz"

    license("GPL-3.0-or-later")

    version("0.15.3", sha256="002750d78ca50fe0f789e24445e10988e16244f81b4f0189bf2fc4ee8b680be5")
    version(
        "0.11.2",
        sha256="a179df1f5803b42bbbb2b50af05ea18ae6fefcbf7020ca2feeb0d3c598a65207",
        url="https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/fastq_screen_v0.11.2.tar.gz",
    )

    variant("bismark", default=False, description="Enable bisulfite mapping with bismark")
    variant("bowtie", default=False, description="Enable mapping with bowtie")
    variant("bwa", default=False, description="Enable mapping with bwa")

    # general dependencies
    depends_on("perl", type="run")
    depends_on("perl-gdgraph", type="run")
    depends_on("bowtie2", type="run")
    depends_on("samtools", type="run")
    # variant dependencies
    depends_on("bismark", type="run", when="+bismark")
    depends_on("bowtie", type="run", when="+bowtie")
    depends_on("bwa", type="run", when="+bwa")

    def patch(self):
        filter_file("/usr/bin/perl", self.spec["perl"].command.path, "fastq_screen", backup=False)

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
