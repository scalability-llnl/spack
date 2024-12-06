# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Orthofiller(Package):
    """OrthoFiller: Identifying missing annotations for evolutionarily
    conserved genes."""

    homepage = "https://github.com/mpdunne/orthofiller/"
    url = "https://github.com/mpdunne/orthofiller/archive/1.1.4.tar.gz"

    license("GPL-3.0-only")

    version("1.1.4", sha256="a693a3372a3f05041ce30cbf84da1be88e85eae4effe32dbd7809ccef119a295")

    depends_on("augustus", type="run")
    depends_on("bedtools2@2.25.0", type="run")
    depends_on("hmmer", type="run")
    depends_on("orthofinder", type="run")
    depends_on("python@2.7:", type="run")
    depends_on("py-biopython", type="run")
    depends_on("py-scipy", type="run")
    depends_on("r", type="run")
    depends_on("r-gamlss", type="run")
    depends_on("mafft", type="run")

    def install(self, spec, prefix):
        # orthofiller tests for common unix programs using man
        # runtime modules will quickly overflow the maximum MANPATH;
        # we change the man tests to use which instead, more reliable anyway
        filter_file('"man "', '"which "', "OrthoFiller.py", string=True)

        os.chmod("OrthoFiller.py", 0o755)
        mkdirp(prefix.bin)
        install("OrthoFiller.py", prefix.bin)
