# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Seqprep(MakefilePackage):
    """SeqPrep is a program to merge paired end Illumina reads that are
    overlapping into a single longer read."""

    homepage = "https://github.com/jstjohn/SeqPrep"
    url = "https://github.com/jstjohn/SeqPrep/archive/v1.3.2.tar.gz"

    license("MIT")

    version("1.3.2", sha256="2b8a462a0e0a3e51f70be7730dc77b1f2bb69e74845dd0fbd2110a921c32265a")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api", type="link")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("SeqPrep", prefix.bin)
