# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Possvm(Package):
    """Possvm (Phylogenetic Ortholog Sorting with Species oVerlap and MCL)
    is a python tool to analyse pre-computed gene trees and identify pairs
    and clusters of orthologous genes. It takes advantage of the species
    overlap algorithm implemented in the ETE toolkit to parse the phylogeny
    and identify orthologous gene pairs, and MCL clustering for orthogroup
    identification."""

    homepage = "https://github.com/xgrau/possvm-orthology"
    git = "https://github.com/xgrau/possvm-orthology.git"

    license("GPL-3.0-only", checked_by="A-N-Other")

    # version number is taken from -v/--version argparse info in possvm.py
    version("1.2", commit="3158757423edafc29aa29bf3ae0cc63a93a56df9")

    depends_on("python@3.10:", type="run")

    # dependencies from GitHub README.md
    depends_on("py-ete3@3.1.2", type="run")
    depends_on("py-markov-clustering@0.0.6.dev0", type="run")
    depends_on("py-matplotlib@3.7.1", type="run")
    depends_on("py-networkx@3.0", type="run")
    depends_on("py-scipy@1.10.0", type="run")
    depends_on("py-numpy@1.23.5", type="run")
    depends_on("py-pandas@1.5.3", type="run")

    def install(self, spec, prefix):
        # This package has no setup.py ...
        # Add shebangs, ensure +x, and move the scripts to prefix.bin
        mkdirp(prefix.bin)
        sed = Executable("sed")
        targets = ("possvm.py", join_path("scripts", "possvm_reconstruction.py"))
        for script in targets:
            sed("-i", rf'1 i\#! {self.spec["python"].command.path}\n', script)
            os.chmod(script, 0o755)
            install(script, prefix.bin)
