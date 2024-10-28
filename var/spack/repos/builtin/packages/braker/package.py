# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Braker(Package):
    """BRAKER is a pipeline for unsupervised RNA-Seq-based genome annotation
    that combines the advantages of GeneMark-ET and AUGUSTUS"""

    homepage = "http://exon.gatech.edu/braker1.html"
    url = "https://github.com/Gaius-Augustus/BRAKER/archive/v2.1.4.tar.gz"
    list_url = "http://bioinf.uni-greifswald.de/augustus/binaries/old"

    license("Artistic-1.0")

    version("2.1.6", sha256="eef3c4037364472988a010322cbd79b5171158f9c016f4383809adade4866c06")
    version("2.1.4", sha256="d48af5649cc879343046f9ddf180fe2c709b5810e0b78cf314bf298514d31d52")
    version(
        "1.11",
        sha256="cb2d9abe1720ed58753d362eee4af3791007efc617754804882d31f9fe2eab00",
        url="https://bioinf.uni-greifswald.de/augustus/binaries/old/BRAKER1_v1.11.tar.gz",
    )

    depends_on("perl", type=("build", "run"))
    depends_on("perl-scalar-util-numeric", type=("build", "run"))
    depends_on("perl-parallel-forkmanager", type=("build", "run"))
    depends_on("perl-file-which", type=("build", "run"))
    depends_on("perl-yaml", type=("build", "run"))
    depends_on("perl-hash-merge", type=("build", "run"))
    depends_on("perl-logger-simple", type=("build", "run"))
    depends_on("perl-file-homedir", when="@2.1.4:", type=("build", "run"))
    depends_on("perl-list-moreutils", when="@2.1.6:", type=("build", "run"))
    depends_on("augustus")
    depends_on("augustus@3.2.3", when="@:2.1.0")
    depends_on("genemark-et")
    depends_on("bamtools")
    depends_on("samtools")
    depends_on("diamond")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        if self.version < Version("2.1.2"):
            install("braker.pl", prefix.bin)
            install("filterGenemark.pl", prefix.bin)
            install("filterIntronsFindStrand.pl", prefix.bin)
            install("helpMod.pm", prefix.lib)
        else:
            install_tree("docs", prefix.docs)
            install_tree("example", prefix.example)
            with working_dir("scripts"):
                install("helpMod.pm", prefix.lib)
                install("*.pl", prefix.bin)

    @run_after("install")
    def filter_sbang(self):
        with working_dir(self.prefix.bin):
            pattern = "^#!.*/usr/bin/env perl"
            repl = "#!{0}".format(self.spec["perl"].command.path)
            files = glob.iglob("*.pl")
            filter_file(pattern, repl, *files, backup=False)

    def setup_run_environment(self, env):
        env.prepend_path("PERL5LIB", self.prefix.lib)
