# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Treesub(Package):
    """A small program (which glues together other programs) that
    allows a user to input a codon alignment in FASTA format and
    produce an annotated phylogenetic tree showing which substitutions
    occurred on a given branch. Originally written for colleagues at
    the MRC NIMR."""

    homepage = "https://github.com/tamuri/treesub"
    url = "https://github.com/tamuri/treesub/archive/v0.2.tar.gz"

    version("0.2", sha256="58b0d2638cf9ae1ad8705df26a57c32b52a69f50e7954debbd678c82772fdc56")
    version("0.1", sha256="c083ecc5f7e9f11645a7e768f6a09fefcbb254b526212003527b4b8dd14723f1")

    depends_on("java", type=("build", "run"))
    depends_on("ant", type="build")
    depends_on("paml", type="run")
    depends_on("raxml", type="run")
    depends_on("figtree", type="run")

    def install(self, spec, prefix):
        ant = self.spec["ant"].command
        ant("jar")

        mkdirp(prefix.bin)
        install_tree("dist", prefix.bin)

        mkdirp(prefix.lib)
        install_tree("lib", prefix.lib)

        execscript = join_path(self.package_dir, "treesub")
        os.chmod(execscript, 0o775)
        install(execscript, prefix.bin)
