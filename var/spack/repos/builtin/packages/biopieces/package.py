# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Biopieces(Package):
    """The Biopieces are a collection of bioinformatics tools that can be
    pieced together in a very easy and flexible manner to perform both
    simple and complex tasks."""

    homepage = "https://maasha.github.io/biopieces/"
    git = "https://github.com/maasha/biopieces.git"

    license("GPL-2.0-only")

    version("2016-04-12", commit="982f80f7c55e2cae67737d80fe35a4e784762856", submodules=True)

    depends_on("c", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    depends_on("perl-module-build", type=("build", "run"))
    depends_on("perl-bit-vector", type=("build", "run"))
    depends_on("perl-svg", type=("build", "run"))
    depends_on("perl-termreadkey", type=("build", "run"))
    depends_on("perl-time-hires", type=("build", "run"))
    depends_on("perl-dbi", type=("build", "run"))
    depends_on("perl-xml-parser", type=("build", "run"))
    depends_on("perl-carp-clan", type=("build", "run"))
    depends_on("perl-class-inspector", type=("build", "run"))
    depends_on("perl-html-parser", type=("build", "run"))
    depends_on("perl-libwww-perl", type=("build", "run"))
    depends_on("perl-soap-lite", type=("build", "run"))
    depends_on("perl-uri", type=("build", "run"))
    depends_on("perl-inline", type=("build", "run"))
    depends_on("perl-inline-c", type=("build", "run"))
    depends_on("perl-parse-recdescent", type=("build", "run"))
    depends_on("perl-perl-version", type=("build", "run"))
    depends_on("perl-db-file", type=("build", "run"))
    depends_on("perl-dbd-mysql", type=("build", "run"))

    depends_on("ruby@1.9:")
    depends_on("ruby-gnuplot")
    depends_on("ruby-narray")
    depends_on("ruby-rubyinline")
    depends_on("ruby-terminal-table")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("blast-plus")
    depends_on("muscle")
    depends_on("mummer")
    depends_on("blat")
    depends_on("vmatch")
    depends_on("bowtie")
    depends_on("bwa")
    depends_on("usearch")
    depends_on("velvet")
    depends_on("idba")
    depends_on("ray")
    depends_on("scan-for-matches")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        # Note: user will need to set environment variables on their own,
        # dependent on where they will want data to be located:
        #    BP_DATA - Contains genomic data etc.
        #    BP_TMP - Required temporary directory
        #    BP_LOG - Required log directory
        env.prepend_path("BP_DIR", self.prefix)
