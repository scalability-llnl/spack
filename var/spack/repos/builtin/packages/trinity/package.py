# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trinity(MakefilePackage):
    """Trinity, developed at the Broad Institute and the Hebrew University of
    Jerusalem, represents a novel method for the efficient and robust de
    novo reconstruction of transcriptomes from RNA-seq data. Trinity
    combines three independent software modules: Inchworm, Chrysalis, and
    Butterfly, applied sequentially to process large volumes of RNA-seq
    reads. Trinity partitions the sequence data into many individual de
    Bruijn graphs, each representing the transcriptional complexity at a
    given gene or locus, and then processes each graph independently to
    extract full-length splicing isoforms and to tease apart transcripts
    derived from paralogous genes.
    """

    homepage = "https://trinityrnaseq.github.io/"
    url = "https://github.com/trinityrnaseq/trinityrnaseq/archive/Trinity-v2.6.6.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.15.1.FULL",
        sha256="ba37e5f696d3d54e8749c4ba439901a3e97e14a4314a5229d7a069ad7b1ee580",
        url="https://github.com/trinityrnaseq/trinityrnaseq/releases/download/Trinity-v2.15.1/trinityrnaseq-v2.15.1.FULL.tar.gz",
    )
    version(
        "2.15.0.FULL",
        sha256="d67de43e535e1173be75de98dcfbdab0bf67f814c9e465a44dfd056cefeb529d",
        url="https://github.com/trinityrnaseq/trinityrnaseq/releases/download/Trinity-v2.15.0/trinityrnaseq-v2.15.0.FULL.tar.gz",
    )
    version(
        "2.14.0.FULL",
        sha256="8adf0c6890f9c9b29c21080dee29a174c60a9e32f5f2a707af86bac4c9fca4ea",
        url="https://github.com/trinityrnaseq/trinityrnaseq/releases/download/Trinity-v2.14.0/trinityrnaseq-v2.14.0.FULL.tar.gz",
    )
    version(
        "2.12.0.FULL",
        sha256="0d47dc433cc3003e1c732b97da605e29c6ccafa38cd52cdb8ecc42399a9195d0",
        url="https://github.com/trinityrnaseq/trinityrnaseq/releases/download/v2.12.0/trinityrnaseq-v2.12.0.FULL.tar.gz",
    )
    version("2.6.6", sha256="868dfadeefaf2d3c6150a88d5e86fbc09466d69bbf4a65f70b4f5a7485668984")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("java@8:", type=("build", "run"))
    depends_on("bowtie2")
    depends_on("jellyfish")
    depends_on("salmon")
    depends_on("perl+threads", type=("build", "run"))
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    # There is no documented list of these deps, but they're in the Dockerfile
    #  and we have runtime errors without them
    # https://github.com/trinityrnaseq/trinityrnaseq/blob/master/Docker/Dockerfile
    depends_on("r-dexseq", type="run", when="@2.12")
    depends_on("star", type="run", when="@2.12")
    depends_on("picard", type="run", when="@2.12")
    depends_on("subread", type="run", when="@2.12")
    depends_on("gatk", type="run", when="@2.12")
    depends_on("gmap-gsnap", type="run", when="@2.12")
    depends_on("r-tximport", type="run", when="@2.12")
    depends_on("r-tximportdata", type="run", when="@2.12")
    depends_on("blast-plus", type="run")
    depends_on("bowtie", type="run")
    depends_on("r", type="run")
    depends_on("r-tidyverse", type="run")
    depends_on("r-edger", type="run")
    depends_on("r-deseq2", type="run")
    depends_on("r-ape", type="run")
    depends_on("r-gplots", type="run")
    depends_on("r-biobase", type="run")
    depends_on("r-qvalue", type="run")
    depends_on("rsem", type="run")
    depends_on("kallisto", type="run")
    depends_on("fastqc", type="run")
    depends_on("samtools", type="run")
    depends_on("py-numpy", type="run")
    depends_on("express", type="run")
    depends_on("perl-db-file", type="run")
    depends_on("perl-uri", type="run")
    depends_on("r-fastcluster", type="run")
    depends_on("r-ctc", type="run")
    depends_on("r-goseq", type="run")
    depends_on("r-glimma", type="run")
    depends_on("r-rots", type="run")
    depends_on("r-goplot", type="run")
    depends_on("r-argparse", type="run")
    depends_on("r-sm", type="run")

    patch("2.15.1.patch", when="@2.15.1.FULL")

    def build(self, spec, prefix):
        make()
        make("trinity_essentials")
        make("plugins")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
        force_remove(join_path(prefix.bin, ".gitmodules"))
        force_remove(join_path(prefix.bin, "Butterfly", ".err"))
        force_remove(join_path(prefix.bin, "Butterfly", "src", ".classpath"))
        force_remove(join_path(prefix.bin, "Butterfly", "src", ".err"))
        force_remove(join_path(prefix.bin, "Butterfly", "src", ".project"))
        remove_linked_tree(join_path(prefix.bin, "Butterfly", "src", ".settings"))
        remove_linked_tree(join_path(prefix.bin, "Inchworm", "src", ".deps"))
        remove_linked_tree(
            join_path(prefix.bin, "trinity-plugins", "ParaFly-0.1.0", "src", ".deps")
        )
        force_remove(join_path(prefix.bin, "trinity-plugins", "seqtk-trinity-0.0.2", ".gitignore"))
        force_remove(join_path(prefix.bin, "trinity-plugins", "slclust", "bin", ".hidden"))

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", self.compiler.openmp_flag)

    def setup_run_environment(self, env):
        env.set("TRINITY_HOME", self.prefix.bin)
        env.prepend_path("PATH", self.prefix.bin.util)
