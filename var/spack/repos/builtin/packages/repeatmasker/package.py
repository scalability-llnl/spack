# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Repeatmasker(Package):
    """RepeatMasker is a program that screens DNA sequences for interspersed
    repeats and low complexity DNA sequences."""

    homepage = "https://www.repeatmasker.org"

    license("OSL-2.1")

    version("4.1.5", sha256="16e07f9efd99adf15f4492b0e334df5ad4ea6ca38ddf62bdd180d257f2f4753f")
    version("4.1.2-p1", sha256="4be54bf6c050422b211e24a797feb06fd7954c8b4ee6f3ece94cb6faaf6b0e96")
    version("4.0.9", sha256="8d67415d89ed301670b7632ea411f794c6e30d8ed0f007a726c4b0a39c8638e5")
    version("4.0.7", sha256="16faf40e5e2f521146f6692f09561ebef5f6a022feb17031f2ddb3e3aabcf166")

    variant("crossmatch", description="Enable CrossMatch search engine", default=False)

    depends_on("perl", type=("build", "run"))
    depends_on("perl-text-soundex", type=("build", "run"))
    depends_on("hmmer")
    depends_on("ncbi-rmblastn")
    depends_on("trf")
    depends_on("python", when="@4.1:", type=("build", "run"))
    depends_on("py-h5py", when="@4.1:", type=("build", "run"))

    depends_on("phrap-crossmatch-swat", type=("build", "run"), when="+crossmatch")

    patch("utf8.patch", when="@:4.0")

    def url_for_version(self, version):
        if version >= Version("4.1.0"):
            url = "https://www.repeatmasker.org/RepeatMasker/RepeatMasker-{0}.tar.gz"
            return url.format(version)
        else:
            url = "https://www.repeatmasker.org/RepeatMasker/RepeatMasker-open-{0}.tar.gz"
            return url.format(version.dashed)

    def install(self, spec, prefix):
        # Config questions consist of:
        #
        # <PRESS ENTER TO CONTINUE>
        # Enter perl path
        # Enter where repeatmasker is being configured from
        # Enter trf path
        # Add a Search Engine:
        #    1. CrossMatch
        #    2. RMBlast - NCBI Blast with RepeatMasker extensions
        #    3. WUBlast/ABBlast (required by DupMasker)
        #    4. HMMER3.1 & DFAM
        #    5. Done
        # Enter RMBlast path
        # Do you want RMBlast to be your default search engine for
        #    Repeatmasker? (Y/N)
        # Add a Search Engine: Done

        config_answers = []

        if spec.satisfies("@:4.0.7"):
            # 4.0.9 removes a bunch of the interactive options
            config_answers.extend(["", self.spec["perl"].command.path, self.stage.source_path])

        # set path to trf
        config_answers.append(self.spec["trf"].prefix.bin.trf)

        # add crossmatch search
        if "+crossmatch" in spec:
            crossmatch = self.spec["phrap-crossmatch-swat"].prefix.bin
            config_answers.extend(["1", crossmatch, "N"])

        # set default BLAST search
        config_answers.extend(["2", self.spec["ncbi-rmblastn"].prefix.bin, "Y"])

        # set non-default HMMER search
        if spec.satisfies("@4.0.9:"):
            config_answers.extend(["3", self.spec["hmmer"].prefix.bin, "N"])
        else:
            config_answers.extend(["4", self.spec["hmmer"].prefix.bin, "N"])

        # end configuration
        config_answers.append("5")

        config_answers_filename = "spack-config.in"

        with open(config_answers_filename, "w") as f:
            f.write("\n".join(config_answers))

        with open(config_answers_filename, "r") as f:
            perl = which("perl")
            perl("configure", input=f)

        # fix perl paths
        # every sbang points to perl, so a regex will suffice
        for f in glob.glob("*.pm"):
            filter_file("#!.*", "#!%s" % spec["perl"].command, f)

        install_tree(".", prefix.bin)
