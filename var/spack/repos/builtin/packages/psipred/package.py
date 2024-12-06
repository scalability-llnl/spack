# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psipred(MakefilePackage):
    """PSIPRED is a simple and accurate secondary structure prediction method, incorporating
    two feed-forward neural networks which perform an analysis on output obtained from
    PSI-BLAST (Position Specific Iterated - BLAST). Using a very stringent cross validation
    method to evaluate the methods performance"""

    homepage = "http://bioinf.cs.ucl.ac.uk/psipred/"
    url = "http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/psipred.4.02.tar.gz"

    license_url = "http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/LICENSE"

    version("4.02", sha256="b4009b6a5f8b76c6d60ac91c4a743512d844864cf015c492fb6d1dc0d092c467")

    depends_on("c", type="build")  # generated

    variant("blast-plus", default=False, description="Use blast-plus in place of blast-legacy")

    depends_on("blast-legacy", type="run", when="~blast-plus")
    depends_on("blast-plus", type="run", when="+blast-plus")

    build_directory = "src"

    # patch to fix segfault on input lines >256 chars
    # https://github.com/psipred/psipred/pull/8
    patch(
        "https://github.com/psipred/psipred/commit/cee0f2c.patch?full_index=1",
        sha256="ef75999f688eaf7984e17f663c17c13e4eaba98912a904be128f562a7eaf8315",
        when="@:1.10.1%gcc@13:",
        level=1,
    )

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file(r"CC\s+= cc", f"CC = {spack_cc}", "Makefile")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("all")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            for f in ("psipred", "psipass2", "chkparse", "seq2mtx"):
                install(f, prefix.bin)

    @run_after("install")
    def configure(self):
        # install data sources
        install_tree("data", prefix.data)
        # modify and install the relevant helper script examples
        mkdir(self.prefix.scripts)
        if self.spec.satisfies("~blast-plus"):
            script = FileFilter("runpsipred")
            blast_location = self.spec["blast-legacy"].prefix.bin
        else:  # +blast-plus
            script = FileFilter(join_path("BLAST+", "runpsipredplus"))
            blast_location = self.spec["blast-plus"].prefix.bin
        script.filter("set dbname .*", "set dbname = ")
        script.filter("set ncbidir .*", f"set ncbidir = {blast_location}")
        script.filter("set execdir .*", f"set execdir = {self.prefix.bin}")
        script.filter("set datadir .*", f"set datadir = {self.prefix.data}")
        if self.spec.satisfies("~blast-plus"):
            install("runpsipred", self.prefix.scripts)
        else:  # +blast-plus
            install(join_path("BLAST+", "runpsipredplus"), self.prefix.scripts)
