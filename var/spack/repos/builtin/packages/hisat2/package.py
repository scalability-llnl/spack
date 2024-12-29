# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Hisat2(MakefilePackage):
    """HISAT2 is a fast and sensitive alignment program for mapping
    next-generation sequencing reads (whole-genome, transcriptome, and
    exome sequencing data) against the general human population (as well as
    against a single reference genome)."""

    homepage = "https://daehwankimlab.github.io/hisat2/"
    url = "ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.1.0-source.zip"

    license("GPL-3.0-or-later")

    version(
        "2.2.1",
        sha256="48e933330d4d8470d2b3dfe7ec3918f2e98a75f7381891e23b7df1fb4f135eb1",
        url="https://cloud.biohpc.swmed.edu/index.php/s/fE9QCsX3NH4QwBi/download",
        extension="zip",
    )
    version(
        "2.2.0",
        sha256="0dd55168853b82c1b085f79ed793dd029db163773f52272d7eb51b3b5e4a4cdd",
        url="https://cloud.biohpc.swmed.edu/index.php/s/hisat2-220-source/download",
        extension="zip",
    )
    version(
        "2.1.0",
        sha256="89a276eed1fc07414b1601947bc9466bdeb50e8f148ad42074186fe39a1ee781",
        url="ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.1.0-source.zip",
        extension="zip",
    )

    variant("sra", default=False, description="Add SRA (Sequence Read Archive) support")

    depends_on("perl", type="run")
    depends_on("python", type="run")

    depends_on("sra-tools", when="+sra")
    depends_on("ncbi-vdb", when="+sra")

    # patch to get SRA working
    patch("sra.patch", when="+sra")

    @when("+sra")
    def build(self, spec, prefix):
        make(
            "USE_SRA=1",
            f"NCBI_NGS_DIR={spec['sra-tools'].prefix}",
            f"NCBI_VDB_DIR={spec['ncbi-vdb'].prefix}",
        )

    def install(self, spec, prefix):
        if spec.satisfies("@:2.1.0"):
            install_tree("doc", prefix.doc)

        install_tree("example", prefix.example)
        install_tree("scripts", prefix.scripts)

        if spec.satisfies("@:2.2.0"):
            install_tree("hisatgenotype_modules", prefix.hisatgenotype_modules)
            install_tree("hisatgenotype_scripts", prefix.hisatgenotype_scripts)

        mkdirp(prefix.bin)
        install("hisat2", prefix.bin)
        install("hisat2-align-s", prefix.bin)
        install("hisat2-align-l", prefix.bin)
        install("hisat2-build", prefix.bin)
        install("hisat2-build-s", prefix.bin)
        install("hisat2-build-l", prefix.bin)
        install("hisat2-inspect", prefix.bin)
        install("hisat2-inspect-s", prefix.bin)
        install("hisat2-inspect-l", prefix.bin)
        install("*.py", prefix.bin)

        if spec.satisfies("@2.2:"):
            install("hisat2-repeat", prefix.bin)

    @run_after("install")
    def filter_sbang(self):
        with working_dir(self.prefix.bin):
            pattern = "^#!.*/usr/bin/env python"
            repl = f"#!{self.spec['python'].command.path}"
            files = ["hisat2-build", "hisat2-inspect"]
            filter_file(pattern, repl, *files, backup=False)

            pattern = "^#!.*/usr/bin/env perl"
            repl = f"#!{self.spec['perl'].command.path}"
            files = ["hisat2"]
            filter_file(pattern, repl, *files, backup=False)

            pattern = "^#!.*/usr/bin/env python3"
            repl = f"#!{self.spec['python'].command.path}"
            files = glob.glob("*.py")
            filter_file(pattern, repl, *files, backup=False)

        with working_dir(self.prefix.scripts):
            pattern = "^#!.*/usr/bin/perl"
            repl = f"#!{self.spec['perl'].command.path}"
            files = glob.glob("*.pl")
            filter_file(pattern, repl, *files, backup=False)
