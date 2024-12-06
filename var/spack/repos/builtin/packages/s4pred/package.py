# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class S4pred(Package):
    """A tool for accurate prediction of a protein's secondary structure from only its amino
    acid sequence with no evolutionary information"""

    homepage = "http://bioinf.cs.ucl.ac.uk/psipred/"
    url = "https://github.com/psipred/s4pred/archive/refs/tags/v1.2.0.tar.gz"

    license("GPL-3.0-only", checked_by="A-N-Other")

    version("1.2.0", sha256="133d4710cef8c58fa603bdedcd41dbd060d9afc029dd181a5bd43f6539783a89")

    depends_on("python", type="run")

    depends_on("py-torch@1.5.1:", type="run")
    depends_on("py-biopython@1.78:", type="run")

    resource(
        name="weights",
        url="http://bioinfadmin.cs.ucl.ac.uk/downloads/s4pred/weights.tar.gz",
        sha256="6a91e887c01bac41b11249ae098fe0d43bcb9e3e15c746758a24a3299fe20283",
    )

    def install(self, spec, prefix):
        # This package has no setup.py, so...
        mkdirp(prefix.bin)
        # unpack resources and correct hardcoded location
        install_tree("weights", prefix.weights)
        filter_file("/weights/", "/../weights/", "run_model.py")
        # add shebang and ensure +x for the main script
        sed = Executable("sed")
        sed("-i", rf'1 i\#! {self.spec["python"].command.path}\n', "run_model.py")
        os.chmod("run_model.py", 0o755)
        # install files and make convenience symlink
        install("*.py", prefix.bin)
        os.symlink(join_path(prefix.bin, "run_model.py"), join_path(prefix.bin, "s4pred"))
