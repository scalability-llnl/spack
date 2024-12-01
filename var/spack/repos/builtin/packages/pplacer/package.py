# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pplacer(Package):
    """Pplacer places query sequences on a fixed reference phylogenetic tree
    to maximize phylogenetic likelihood or posterior probability according
    to a reference alignment. Pplacer is designed to be fast, to give
    useful information about uncertainty, and to offer advanced
    visualization and downstream analysis.
    """

    homepage = "https://matsen.fhcrc.org/pplacer/"
    url = "https://github.com/matsen/pplacer/releases/download/v1.1.alpha19/pplacer-linux-v1.1.alpha19.zip"

    version(
        "1.1.alpha19", sha256="9131b45c35ddb927f866385f149cf64af5dffe724234cd4548c22303a992347d"
    )

    def install(self, spec, prefix):
        install_tree("scripts", prefix.bin)
        force_remove(join_path(prefix.bin, "setup.py"))
        install("guppy", prefix.bin)
        install("pplacer", prefix.bin)
        install("rppr", prefix.bin)
