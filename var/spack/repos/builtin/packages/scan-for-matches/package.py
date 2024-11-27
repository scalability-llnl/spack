# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ScanForMatches(Package):
    """scan_for_matches is a utility written in C for locating patterns in DNA
    or protein FASTA files."""

    homepage = "https://blog.theseed.org/servers/2010/07/scan-for-matches.html"
    url = "https://www.theseed.org/servers/downloads/scan_for_matches.tgz"

    version("2010-7-16", sha256="c6b17930efbdfbac28b57c3a0b4f8c26effb36c48988d82e41c81c6962e2d68f")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        cc = Executable(self.compiler.cc)
        cc("-O", "-o", "scan_for_matches", "ggpunit.c", "scan_for_matches.c")
        mkdirp(prefix.bin)
        install("scan_for_matches", prefix.bin)
