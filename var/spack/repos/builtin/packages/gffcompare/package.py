# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gffcompare(MakefilePackage):
    """gffcompare: classify, merge, tracking and annotation of GFF files by comparing to a
    reference annotation GFF"""

    homepage = "https://ccb.jhu.edu/software/stringtie/gffcompare.shtml"
    url = (
        "https://github.com/gpertea/gffcompare/releases/download/v0.12.6/gffcompare-0.12.6.tar.gz"
    )

    license("MIT")

    version("0.12.6", sha256="0e713bc9177d874c935802d11669776da5e9377a8c4d031153b48a783d3391d0")

    depends_on("cxx", type="build")  # generated

    def build(self, spec, prefix):
        make("release")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("gffcompare", prefix.bin)
        install("trmap", prefix.bin)
