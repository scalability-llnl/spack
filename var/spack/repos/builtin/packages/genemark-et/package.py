# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class GenemarkEt(Package):
    """Gene Prediction in Bacteria, archaea, Metagenomes and
    Metatranscriptomes.
    When downloaded this file is named the same for all versions.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://topaz.gatech.edu/GeneMark"
    manual_download = True

    version("4.69", sha256="027a060d6e0654d4d2a09bc97dde9bd6efd60bc4dc3e0183f212ddd5e6854ae7")
    version("4.65", sha256="62ea2dfa1954ab25edcc118dbeaeacf15924274fb9ed47bc54716cfd15ad04fe")
    version("4.46", sha256="856b0b6c7cbd12835e140ff04ecd9124376348efd65f76bfd8b8e08c1834eac0")
    version("4.38", sha256="cee3bd73d331be44159eac15469560d0b07ffa2c98ac764c37219e1f3b7d3146")

    depends_on("perl", type=("build", "run"))
    depends_on("perl-yaml", type=("build", "run"))
    depends_on("perl-hash-merge", type=("build", "run"))
    depends_on("perl-parallel-forkmanager", type=("build", "run"))
    depends_on("perl-logger-simple", when="@:4.46", type=("build", "run"))
    depends_on("perl-mce", when="@4.65:", type=("build", "run"))
    depends_on("perl-thread-queue", when="@4.65:", type=("build", "run"))
    depends_on("perl-threads", when="@4.65:", type=("build", "run"))

    def url_for_version(self, version):
        if version >= Version("4.65"):
            return "file://{0}/gmes_linux_64.tar.gz".format(os.getcwd())
        else:
            return "file://{0}/gm_et_linux_64.tar.gz".format(os.getcwd())

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.bin.heu_dir)
        if self.version <= Version("4.38"):
            source_dir = "gmes_petap"
        else:
            source_dir = self.stage.source_path
        with working_dir(source_dir):
            install_tree("lib", prefix.lib)
            files = glob.iglob("*")
            for file in files:
                if os.path.isfile(file):
                    install(file, prefix.bin)
            install_tree("heu_dir", prefix.bin.heu_dir)

    @run_after("install")
    def filter_sbang(self):
        with working_dir(self.prefix.bin):
            pattern = "^#!.*/usr/bin/perl"
            repl = "#!{0}".format(self.spec["perl"].command.path)
            files = glob.iglob("*.pl")
            filter_file(pattern, repl, *files, backup=False)

    def setup_run_environment(self, env):
        env.prepend_path("PERL5LIB", self.prefix.lib)
