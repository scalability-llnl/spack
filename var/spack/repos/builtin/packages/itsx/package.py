# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Itsx(Package):
    """Improved software detection and extraction of ITS1 and ITS2 from
    ribosomal ITS sequences of fungi and other eukaryotes for use in
    environmental sequencing"""

    homepage = "https://microbiology.se/software/itsx/"
    url = "https://microbiology.se/sw/ITSx_1.0.11.tar.gz"

    license("GPL-3.0-or-later")

    version("1.0.11", sha256="8f4f76fc9c43b61f4dd4cd8dc4e495e9687943e15515396583f7a757651d435e")

    depends_on("perl", type=("build", "run"))
    depends_on("hmmer")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ITSx", prefix.bin)
        install_tree("ITSx_db", prefix.bin.ITSx_db)
