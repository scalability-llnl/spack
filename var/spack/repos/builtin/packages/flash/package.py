# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flash(MakefilePackage):
    """FLASH (Fast Length Adjustment of SHort reads) is a very
    fast and accurate software tool to merge paired-end reads
    from next-generation sequencing experiments."""

    homepage = "https://ccb.jhu.edu/software/FLASH/"
    url = "https://sourceforge.net/projects/flashpage/files/FLASH-1.2.11.tar.gz"

    license("GPL-3.0-or-later")

    version("1.2.11", sha256="685ca6f7fedda07434d8ee03c536f4763385671c4509c5bb48beb3055fd236ac")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("flash", prefix.bin)
