# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Isescan(Package):
    """A python pipeline to identify IS (Insertion Sequence) elements in
    genome and metagenome"""

    homepage = "https://github.com/xiezhq/ISEScan"
    url = "https://github.com/xiezhq/ISEScan/archive/refs/tags/v1.7.2.1.tar.gz"

    license("Apache-2.0")

    version("1.7.2.3", sha256="90ef6bc660e471347f65864bd3563f769ed4b79b1a932195f353c5e86351ab05")
    version("1.7.2.1", sha256="b971a3e86a8cddaa4bcd520ba9e75425bbe93190466f81a3791ae0cb4baf5e5d")

    depends_on("c", type="build")  # generated

    depends_on("python@3.3.3:", type="run")
    depends_on("py-numpy@1.8.0:", type="run")
    depends_on("py-scipy@0.13.1:", type="run")
    depends_on("py-biopython@1.62:", type="run")
    depends_on("py-fastcluster", type="run")
    depends_on("blast-plus@2.2.31:", type="run")
    depends_on("fraggenescan@:1.30", type="run")
    depends_on("hmmer@3.1b2:", type="run")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "ssw201507"))

    def install(self, spec, prefix):
        # build bundled SSW library
        with working_dir("ssw201507"):
            Executable(spack_cc)(
                "-O3",
                "-pipe",
                self.compiler.cc_pic_flag,
                "-shared",
                "-rdynamic",
                "-o",
                "libssw." + dso_suffix,
                "ssw.c",
                "ssw.h",
            )

        # set paths to required programs
        blast_pfx = self.spec["blast-plus"].prefix.bin
        blastn_path = blast_pfx.blastn
        blastp_path = blast_pfx.blastp
        makeblastdb_path = blast_pfx.makeblastdb

        hmmer_pfx = self.spec["hmmer"].prefix.bin
        phmmer_path = hmmer_pfx.phmmer
        hmmsearch_path = hmmer_pfx.hmmsearch

        fgs_pfx = self.spec["fraggenescan"].prefix.bin
        fgs_path = join_path(fgs_pfx, "run_FragGeneScan.pl")

        constants = FileFilter("constants.py")

        constants.filter("/apps/inst/FragGeneScan1.30/run_FragGeneScan.pl", fgs_path, string=True)
        constants.filter("/apps/inst/hmmer-3.3/bin/phmmer", phmmer_path, string=True)
        constants.filter("/apps/inst/hmmer-3.3/bin/hmmsearch", hmmsearch_path, string=True)
        constants.filter("/apps/inst/ncbi-blast-2.10.0+/bin/blastn", blastn_path, string=True)
        constants.filter("/apps/inst/ncbi-blast-2.10.0+/bin/blastp", blastp_path, string=True)
        constants.filter(
            "/apps/inst/ncbi-blast-2.10.0+/bin/makeblastdb", makeblastdb_path, string=True
        )

        # install the whole tree
        install_tree(".", prefix)
        set_executable(join_path(prefix, "isescan.py"))
