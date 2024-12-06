# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gblocks(Package):
    """Gblocks is a computer program written in ANSI C language that eliminates
    poorly aligned positions and divergent regions of an alignment of DNA or
    protein sequences"""

    homepage = "http://molevol.cmima.csic.es/castresana/Gblocks.html"
    url = "http://molevol.cmima.csic.es/castresana/Gblocks/Gblocks_Linux64_0.91b.tar.Z"

    version("0.91b", sha256="563658f03cc5e76234a8aa705bdc149398defec813d3a0c172b5f94c06c880dc")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("Gblocks", prefix.bin)
