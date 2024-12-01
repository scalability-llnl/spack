# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Phantompeakqualtools(RPackage):
    """This package computes informative enrichment and quality measures for
    ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data."""

    homepage = "https://github.com/kundajelab/phantompeakqualtools"
    url = "https://github.com/kundajelab/phantompeakqualtools/archive/1.2.tar.gz"

    version("1.2", sha256="86cbcca80b65f150b1cdbea673d8a47caba88c2db6b3b567a80f2c797c9a1668")

    depends_on("awk")
    depends_on("samtools")
    depends_on("r", type=("build", "run"))
    depends_on("r-phantompeakqualtools", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("run_spp.R", prefix.bin)
