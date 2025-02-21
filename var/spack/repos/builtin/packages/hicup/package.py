# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hicup(Package):
    """HiCUP: a bioinformatics pipeline for processing Hi-C data"""

    homepage = "https://stevenwingett.github.io/HiCUP"
    url = "https://github.com/StevenWingett/HiCUP/archive/refs/tags/v0.9.2.tar.gz"
    git = "https://github.com/StevenWingett/HiCUP.git"

    license("LGPL-3.0-only", checked_by="A-N-Other")

    version("0.9.2", sha256="7f9f65669d14fd2499afc4ac87735834b57b8f30b8e5785c4b406ec206cf9d2a")
    version("0.8.3", sha256="e2381c2c45e0d79a6d1a2d9a8358b3efe8da727112d262cb0122132012266368")
    version("combinations", branch="combinations")

    variant("bowtie2", description="Use bowtie2 aligner", default=True)
    variant("bowtie", description="Use bowtie aligner", default=False)

    depends_on("pandoc", type="run")
    depends_on("perl", type="run")
    depends_on("perl-math-round", type="run")
    depends_on("r", type="run")
    depends_on("r-stringi@1.7.8:", type="run")
    depends_on("r-markdown", type="run")
    depends_on("r-tidyverse", type="run")
    depends_on("r-plotly", type="run")
    depends_on("samtools@0.1.18:", type="run")
    # variant dependencies
    depends_on("bowtie2", type="run", when="+bowtie2")
    depends_on("bowtie", type="run", when="+bowtie")

    def edit(self, spec, prefix):
        grep = which("grep")
        chmod = which("chmod")
        perl_files = grep("-lRr", "#!/usr/bin/perl", ".").splitlines()
        for f in perl_files:
            filter_file("/usr/bin/perl", self.spec["perl"].command.path, f, backup=False)
            filter_file("$Bin", "$RealBin", f, backup=False)
            chmod("+x", f)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("hicup*", prefix.bin)
        if self.spec.satisfies("@combinations"):
            install("Misc/get_captured_reads", prefix.bin)
        else:
            install("Misc/hicup_capture", prefix.bin)
        install("Conversion/hicup2*", prefix.bin)
        install_tree("r_scripts", prefix.bin.r_scripts)
