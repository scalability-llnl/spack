# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rtax(Package):
    """Rapid and accurate taxonomic classification of short paired-end
    sequence reads from the 16S ribosomal RNA gene"""

    homepage = "https://github.com/davidsoergel/rtax"
    url = "http://static.davidsoergel.com/rtax-0.984.tgz"

    version("0.984", sha256="92ad9a881ca1d17221794b4313654291b30df6a9edcd0453034a090ae13a3442")

    depends_on("usearch")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("rtax", prefix.bin)
        install_tree("scripts", prefix.bin.scripts)
        install_tree("greengenes", prefix.bin.greengenes)
