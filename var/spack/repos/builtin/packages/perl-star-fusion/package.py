# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlStarFusion(Package):
    """STAR-Fusion is a component of the Trinity Cancer Transcriptome Analysis
    Toolkit (CTAT). STAR-Fusion uses the STAR aligner to identify candidate
    fusion transcripts supported by Illumina reads. STAR-Fusion further
    processes the output generated by the STAR aligner to map junction reads
    and spanning reads to a reference annotation set."""

    homepage = "https://github.com/STAR-Fusion/STAR-Fusion"
    git = "https://github.com/STAR-Fusion/STAR-Fusion.git"

    license("BSD-3-Clause")

    version("master", commit="8c5a541ab701debebb68e5c4ee9d6a03e03d65ca")

    extends("perl")

    depends_on("star", type=("build", "run"))
    depends_on("perl", type=("build", "run"))
    depends_on("perl-set-intervaltree", type=("build", "run"))
    depends_on("perl-dbi", type=("build", "run"))
    depends_on("perl-db-file", type=("build", "run"))
    depends_on("perl-uri", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(perl_lib_dir)
        install(join_path("PerlLib", "*.pm"), perl_lib_dir)
        install_tree("util", prefix.bin)
        install("STAR-Fusion", prefix.bin)
