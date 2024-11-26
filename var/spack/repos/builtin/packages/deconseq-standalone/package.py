# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DeconseqStandalone(Package):
    """The DeconSeq tool can be used to automatically detect and efficiently
    remove sequence contaminations from genomic and metagenomic datasets."""

    homepage = "https://deconseq.sourceforge.net"
    url = "https://sourceforge.net/projects/deconseq/files/standalone/deconseq-standalone-0.4.3.tar.gz"

    license("GPL-3.0-only")

    version("0.4.3", sha256="fb4050418c26a5203220f6396263da554326657590cffd65053eb8adc465ac65")

    depends_on("c", type="build")  # generated

    depends_on("perl@5:")

    def install(self, spec, prefix):
        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "deconseq.pl")
        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "splitFasta.pl")

        mkdirp(prefix.bin)
        install("bwa64", prefix.bin)
        install("bwaMAC", prefix.bin)
        install("deconseq.pl", prefix.bin)
        install("splitFasta.pl", prefix.bin)
        install("DeconSeqConfig.pm", prefix)

        chmod = which("chmod")
        chmod("+x", join_path(prefix.bin, "bwa64"))
        chmod("+x", join_path(prefix.bin, "bwaMAC"))
        chmod("+x", join_path(prefix.bin, "deconseq.pl"))
        chmod("+x", join_path(prefix.bin, "splitFasta.pl"))

    def setup_run_environment(self, env):
        env.prepend_path("PERL5LIB", self.prefix)
