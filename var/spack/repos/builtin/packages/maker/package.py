# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Maker(Package):
    """MAKER is a portable and easily configurable genome annotation pipeline.
    It's purpose is to allow smaller eukaryotic and prokaryotic genomeprojects
    to independently annotate their genomes and to create genome databases.
    MAKER identifies repeats, aligns ESTs and proteins to a genome, produces
    ab-initio gene predictions and automatically synthesizes these data into
    gene annotations having evidence-based quality values. MAKER is also easily
    trainable: outputs of preliminary runs can be used to automatically retrain
    its gene prediction algorithm, producing higher quality gene-models on
    subsequent runs. MAKER's inputs are minimal and its ouputs can be directly
    loaded into a GMOD database. They can also be viewed in the Apollo genome
    browser; this feature of MAKER provides an easy means to annotate, view and
    edit individual contigs and BACs without the overhead of a database. MAKER
    should prove especially useful for emerging model organism projects with
    minimal bioinformatics expertise and computer resources.

    Note: MAKER requires registration. Fill out the form at
    http://yandell.topaz.genetics.utah.edu/cgi-bin/maker_license.cgi to get a
    download link. Spack will search your current directory for the download
    file. Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.yandell-lab.org/software/maker.html"
    manual_download = True

    version("3.01.04", sha256="87be5b0fad92d7d7b359f233877830e8a353a80277c3c88aa89f359899fa8bfb")
    version("3.01.03", sha256="d3979af9710d61754a3b53f6682d0e2052c6c3f36be6f2df2286d2587406f07d")
    version("2.31.10", sha256="d3979af9710d61754a3b53f6682d0e2052c6c3f36be6f2df2286d2587406f07d")

    def url_for_version(self, version):
        return "file://{0}/maker-{1}.tgz".format(os.getcwd(), version)

    variant("mpi", default=True, description="Build with MPI support")

    patch("install.patch")
    patch("mpi.patch")
    patch("MpiChunk.patch")

    depends_on("perl", type=("build", "run"))
    depends_on("perl-module-build", type="build")
    depends_on("perl-dbi", type=("build", "run"))
    depends_on("perl-dbd-mysql", type=("build", "run"))
    depends_on("perl-dbd-pg", type=("build", "run"))
    depends_on("perl-dbd-sqlite", type=("build", "run"))
    depends_on("perl-forks", type=("build", "run"))
    depends_on("perl-file-which", type=("build", "run"))
    depends_on("perl-perl-unsafe-signals", type=("build", "run"))
    depends_on("perl-bit-vector", type=("build", "run"))
    depends_on("perl-inline-c", type=("build", "run"))
    depends_on("perl-io-all", type=("build", "run"))
    depends_on("perl-io-prompt", type=("build", "run"))
    depends_on("perl-bioperl", type=("build", "run"))
    depends_on("blast-plus")
    depends_on("snap-korf")
    depends_on("repeatmasker")
    depends_on("exonerate")
    depends_on("augustus")
    depends_on("interproscan@:4.8")
    depends_on("mpi", when="+mpi")

    def install(self, spec, prefix):
        if "+mpi" in spec:
            with working_dir("src"):
                pattern = r"my \$go = 0;"
                repl = "my $go = 1;"
                filter_file(pattern, repl, "Build.PL", backup=False)

        perl = which("perl")
        rm = which("rm")
        with working_dir("src"):
            perl("Build.PL", "--install_base", prefix)
            perl("Build", "install")

        install_tree("lib", join_path(prefix, "perl", "lib"))

        # Remove scripts that do not work. The 'mpi_evaluator' and
        # 'mpi_iprscan' scripts depend on a custom perl module that is not
        # shipped with maker. The 'maker2chado' script depends on setting up a
        # CHADO database which is out of scope here.
        for package in (
            "maker2chado",
            "maker2jbrowse",
            "maker2wap",
            "mpi_evaluator",
            "mpi_iprscan",
        ):
            rm("-f", join_path(prefix.bin, package))

        # Remove old IO::Prompt perl module
        rm("-r", "-f", join_path(prefix, "perl", "lib", "IO"))
