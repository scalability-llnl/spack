# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Kraken(Package):
    """Kraken is a system for assigning taxonomic labels to short DNA
    sequences, usually obtained through metagenomic studies."""

    homepage = "https://ccb.jhu.edu/software/kraken/"
    url = "https://github.com/DerrickWood/kraken/archive/v1.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.1.1", sha256="73e48f40418f92b8cf036ca1da727ca3941da9b78d4c285b81ba3267326ac4ee")
    version("1.0", sha256="bade6d83233c26226d02bd427fe0a4d6cd6dc5c0300927e30d41e885a478c378")

    depends_on("cxx", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    # Does NOT support JELLYFISH 2.0. Ver 1.1.11 is the last version of
    # JELLYFISH 1.
    depends_on("jellyfish@1.1.11", when="@1.0")

    def install(self, spec, prefix):
        installer = Executable("./install_kraken.sh")
        installer(self.stage.source_path)
        mkdirp(prefix.bin)
        files = glob.iglob("*")
        for file in files:
            if os.path.isfile(file):
                install(file, prefix.bin)
